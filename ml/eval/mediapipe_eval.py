"""MediaPipe Holistic feasibility evaluation for SignBridge-TR (Jira SB-15).

Runs MediaPipe Holistic frame by frame on a video and reports:
  - landmark groups, landmarks per group and fields per landmark
  - the per-frame flattened feature-vector size (model input standard)
  - processing FPS on this machine
  - per-group missing-frame percentages, gap lengths and low-visibility stats
  - a simple jitter proxy (frame-to-frame wrist displacement)
Optionally dumps one frame's keypoints to JSON as a concrete example.

Usage:
    python ml/eval/mediapipe_eval.py /path/to/video.mp4 \
        [--dump-json docs/mediapipe_sample_keypoints.json] [--dump-frame N] \
        [--vis-threshold 0.5] [--json-out summary.json]
"""

import argparse
import json
import os
import platform
import sys
import time

import cv2
import mediapipe as mp
import numpy as np

# Landmark groups in the fixed concatenation order used for the feature vector.
# Pose is the only group whose landmarks carry a meaningful visibility score.
GROUPS = [
    # (name, attribute on Holistic results, landmark count, fields)
    ("pose", "pose_landmarks", 33, ("x", "y", "z", "visibility")),
    ("face", "face_landmarks", 468, ("x", "y", "z")),
    ("left_hand", "left_hand_landmarks", 21, ("x", "y", "z")),
    ("right_hand", "right_hand_landmarks", 21, ("x", "y", "z")),
]

# Pose landmark indices relevant to signing (upper body).
POSE_UPPER_BODY = {
    "left_shoulder": 11, "right_shoulder": 12,
    "left_elbow": 13, "right_elbow": 14,
    "left_wrist": 15, "right_wrist": 16,
}


def group_array(landmark_list, count, fields):
    """Convert a MediaPipe landmark list to a (count, len(fields)) array.

    Returns None if the group was not detected in this frame.
    """
    if landmark_list is None:
        return None
    lms = landmark_list.landmark
    if len(lms) != count:
        raise ValueError(f"expected {count} landmarks, got {len(lms)}")
    return np.array([[getattr(lm, f) for f in fields] for lm in lms], dtype=np.float32)


def raw_visibility_stats(landmark_list):
    """Return (has_visibility_field_set, mean raw visibility) for a landmark list."""
    lms = landmark_list.landmark
    has_field = any(lm.HasField("visibility") for lm in lms)
    return has_field, float(np.mean([lm.visibility for lm in lms]))


def flatten_frame(arrays):
    """Concatenate all groups into one fixed-size vector (zero-fill missing groups)."""
    parts = []
    for name, _, count, fields in GROUPS:
        arr = arrays[name]
        if arr is None:
            arr = np.zeros((count, len(fields)), dtype=np.float32)
        parts.append(arr.reshape(-1))
    return np.concatenate(parts)


def longest_run(flags):
    """Length of the longest run of True values in a list of booleans."""
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


def evaluate(video_path, vis_threshold):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sys.exit(f"Could not open video: {video_path}")

    meta = {
        "video": os.path.basename(video_path),
        "source_fps": cap.get(cv2.CAP_PROP_FPS),
        "frame_count_reported": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }

    frames = []         # per-frame dict: group name -> array or None
    raw_vis = {name: [] for name, *_ in GROUPS}   # (has_field, mean_vis) per detection

    holistic = mp.solutions.holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        refine_face_landmarks=False,
    )

    # Time only the decode + inference loop, not model/video setup.
    start = time.perf_counter()
    while True:
        ok, frame_bgr = cap.read()
        if not ok:
            break
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb)

        arrays = {}
        for name, attr, count, fields in GROUPS:
            lm_list = getattr(results, attr)
            arrays[name] = group_array(lm_list, count, fields)
            if lm_list is not None:
                raw_vis[name].append(raw_visibility_stats(lm_list))
        frames.append(arrays)
    elapsed = time.perf_counter() - start
    holistic.close()
    cap.release()

    n = len(frames)
    if n == 0:
        sys.exit("No frames decoded.")
    meta["frames_processed"] = n
    meta["duration_s"] = n / meta["source_fps"] if meta["source_fps"] else None

    # --- Structure / vector size (derived from the actual flattened arrays) ---
    vector_size = int(flatten_frame(frames[0]).shape[0])
    structure = []
    for name, _, count, fields in GROUPS:
        vis = raw_vis[name]
        structure.append({
            "group": name,
            "landmarks": count,
            "fields_used": list(fields),
            "values": count * len(fields),
            "visibility_field_set": any(v[0] for v in vis) if vis else None,
            "mean_raw_visibility": float(np.mean([v[1] for v in vis])) if vis else None,
        })
    pose_hands_size = sum(s["values"] for s in structure if s["group"] != "face")

    # --- Missing groups ---
    missing = {}
    for name, *_ in GROUPS:
        flags = [f[name] is None for f in frames]
        missing[name] = {
            "missing_frames": int(sum(flags)),
            "missing_pct": 100.0 * sum(flags) / n,
            "longest_missing_run": longest_run(flags),
        }
    both_missing = [f["left_hand"] is None and f["right_hand"] is None for f in frames]
    any_missing = [f["left_hand"] is None or f["right_hand"] is None for f in frames]
    hands = {
        "no_hand_pct": 100.0 * sum(both_missing) / n,
        "at_least_one_hand_missing_pct": 100.0 * sum(any_missing) / n,
    }

    # --- Pose visibility ---
    pose_frames = [f["pose"] for f in frames if f["pose"] is not None]
    pose_vis = None
    if pose_frames:
        vis = np.stack([p[:, 3] for p in pose_frames])  # (frames, 33)
        pose_vis = {
            "mean_visibility_all": float(vis.mean()),
            "pct_landmarks_below_threshold_all": 100.0 * float((vis < vis_threshold).mean()),
            "upper_body": {
                k: {
                    "mean": float(vis[:, i].mean()),
                    "pct_frames_below_threshold": 100.0 * float((vis[:, i] < vis_threshold).mean()),
                }
                for k, i in POSE_UPPER_BODY.items()
            },
        }

    # --- Jitter proxy: wrist (landmark 0) displacement between consecutive detected frames ---
    jitter = {}
    for name in ("left_hand", "right_hand"):
        d = []
        for a, b in zip(frames, frames[1:]):
            if a[name] is not None and b[name] is not None:
                d.append(float(np.linalg.norm(b[name][0, :2] - a[name][0, :2])))
        jitter[name] = {
            "pairs": len(d),
            "mean_wrist_disp": float(np.mean(d)) if d else None,
            "max_wrist_disp": float(np.max(d)) if d else None,
        }

    summary = {
        "meta": meta,
        "processing": {"elapsed_s": elapsed, "processing_fps": n / elapsed},
        "structure": structure,
        "vector_size_full": vector_size,
        "vector_size_pose_hands": pose_hands_size,
        "missing": missing,
        "hands": hands,
        "pose_visibility": pose_vis,
        "vis_threshold": vis_threshold,
        "jitter": jitter,
    }
    return summary, frames


def pick_dump_frame(frames, requested):
    """Requested index, else first frame with both hands, else middle frame."""
    if requested is not None:
        return requested
    for i, f in enumerate(frames):
        if f["left_hand"] is not None and f["right_hand"] is not None:
            return i
    return len(frames) // 2


def dump_frame(frames, idx, video_path, out_path):
    f = frames[idx]
    vec = flatten_frame(f)
    data = {
        "source_video": os.path.basename(video_path),
        "frame_index": idx,
        "versions": {
            "python": platform.python_version(),
            "mediapipe": mp.__version__,
            "opencv": cv2.__version__,
            "numpy": np.__version__,
        },
        "concat_order": [g[0] for g in GROUPS],
        "vector_size": int(vec.shape[0]),
        "groups": {},
        "flattened_vector": [round(float(v), 6) for v in vec],
    }
    for name, _, count, fields in GROUPS:
        arr = f[name]
        data["groups"][name] = {
            "detected": arr is not None,
            "landmarks": count,
            "fields": list(fields),
            "data": None if arr is None else [
                [round(float(v), 6) for v in row] for row in arr
            ],
        }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(data, fh, indent=1)
    return data


def print_report(s):
    m = s["meta"]
    print(f"=== {m['video']} ===")
    print(f"Versions: python {platform.python_version()}, mediapipe {mp.__version__}, "
          f"opencv {cv2.__version__}, numpy {np.__version__}")
    print(f"Video: {m['width']}x{m['height']}, source fps {m['source_fps']:.2f}, "
          f"frames {m['frames_processed']} (reported {m['frame_count_reported']}), "
          f"duration {m['duration_s']:.2f}s")
    p = s["processing"]
    print(f"Processing: {p['elapsed_s']:.2f}s -> {p['processing_fps']:.2f} fps")
    print("\nStructure:")
    for g in s["structure"]:
        print(f"  {g['group']:<11} {g['landmarks']:>3} landmarks x {len(g['fields_used'])} "
              f"fields {g['fields_used']} = {g['values']} values | "
              f"visibility field set: {g['visibility_field_set']}, "
              f"mean raw visibility: {g['mean_raw_visibility']}")
    print(f"Flattened vector size (pose+face+hands): {s['vector_size_full']}")
    print(f"Flattened vector size (pose+hands only): {s['vector_size_pose_hands']}")
    print("\nMissing (per group):")
    for k, v in s["missing"].items():
        print(f"  {k:<11} missing {v['missing_frames']:>4} frames ({v['missing_pct']:.1f}%), "
              f"longest gap {v['longest_missing_run']} frames")
    print(f"  no hand detected: {s['hands']['no_hand_pct']:.1f}% of frames; "
          f"at least one hand missing: {s['hands']['at_least_one_hand_missing_pct']:.1f}%")
    pv = s["pose_visibility"]
    if pv:
        print(f"\nPose visibility (threshold {s['vis_threshold']}): mean {pv['mean_visibility_all']:.3f}, "
              f"{pv['pct_landmarks_below_threshold_all']:.1f}% of landmark-frames below threshold")
        for k, v in pv["upper_body"].items():
            print(f"  {k:<15} mean {v['mean']:.3f}, below threshold in "
                  f"{v['pct_frames_below_threshold']:.1f}% of frames")
    print("\nJitter proxy (hand wrist, normalized image units, consecutive detected frames):")
    for k, v in s["jitter"].items():
        if v["pairs"]:
            print(f"  {k:<11} pairs {v['pairs']}, mean {v['mean_wrist_disp']:.4f}, "
                  f"max {v['max_wrist_disp']:.4f}")
        else:
            print(f"  {k:<11} no consecutive detections")


def main():
    ap = argparse.ArgumentParser(description="MediaPipe Holistic feasibility evaluation (SB-15)")
    ap.add_argument("video", help="path to the input video")
    ap.add_argument("--dump-json", help="write one frame's keypoints to this JSON file")
    ap.add_argument("--dump-frame", type=int, default=None,
                    help="frame index to dump (default: first frame with both hands)")
    ap.add_argument("--vis-threshold", type=float, default=0.5,
                    help="pose visibility threshold for low-visibility stats")
    ap.add_argument("--json-out", help="write the full summary as JSON to this file")
    args = ap.parse_args()

    summary, frames = evaluate(args.video, args.vis_threshold)
    print_report(summary)

    if args.dump_json:
        idx = pick_dump_frame(frames, args.dump_frame)
        data = dump_frame(frames, idx, args.video, args.dump_json)
        print(f"\nDumped frame {idx} ({data['vector_size']} values) to {args.dump_json}")
    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump(summary, fh, indent=2)


if __name__ == "__main__":
    main()
