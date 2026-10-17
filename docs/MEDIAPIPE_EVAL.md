# MediaPipe Holistic Feasibility and Data Structure Evaluation (SB-15)

This document evaluates whether MediaPipe Holistic keypoint output is suitable as the input to the SignBridge-TR sign model, and defines the per-frame input format. It is a feasibility and data-structure study, not a sign-recognition accuracy test: MediaPipe does not recognise signs, it only extracts pose, face and hand keypoints.

All numbers below come from actual runs of `ml/eval/mediapipe_eval.py` on the two sample videos.

## 1. Setup and Hands-on Runs

Environment (macOS, Apple M1, arm64):

- Python 3.11.4 in a repo-local virtual environment (`.venv/`, gitignored)
- `mediapipe==0.10.9` (still ships the legacy `mp.solutions.holistic` solution; installed without wheel issues on Python 3.11)
- `opencv-python==5.0.0.93`
- `numpy==2.4.6`
- `protobuf==3.20.3` (pulled in by mediapipe)

Pinned versions are in `ml/eval/requirements.txt`. Holistic was run with `model_complexity=1`, `smooth_landmarks=True`, `refine_face_landmarks=False`.

Sample videos (kept outside the repository, not committed):

| Video | Sign | Resolution | Source FPS | Frames | Duration |
|---|---|---|---|---|---|
| `Ornek_Merhaba.mp4` | merhaba | 324x216 | 25.00 | 150 | 6.00 s |
| `ornek_tesekkur.mp4` | tesekkurler | 324x216 | 25.00 | 127 | 5.08 s |

Reproduce:

```bash
python3.11 -m venv .venv
.venv/bin/pip install -r ml/eval/requirements.txt
.venv/bin/python ml/eval/mediapipe_eval.py /path/to/Ornek_Merhaba.mp4 \
    --dump-json docs/mediapipe_sample_keypoints.json
.venv/bin/python ml/eval/mediapipe_eval.py /path/to/ornek_tesekkur.mp4
```

## 2. Keypoint Output Structure

Holistic returns four landmark groups per frame. Each group is either fully present or entirely missing (`None`) in a given frame.

| Group | Landmarks | Fields used | Values | Visibility |
|---|---|---|---|---|
| pose | 33 | x, y, z, visibility | 132 | Yes (meaningful, 0-1) |
| face | 468 | x, y, z | 1404 | No (field not set, always 0.0) |
| left_hand | 21 | x, y, z | 63 | No (field not set, always 0.0) |
| right_hand | 21 | x, y, z | 63 | No (field not set, always 0.0) |

- `x`, `y`: normalised to image width/height (roughly 0-1; can fall outside when a landmark is estimated off-frame).
- `z`: relative depth. For pose it is relative to the hip midpoint; for hands it is relative to the wrist; for face it is relative to the face centre. It is less reliable than `x`/`y`.
- `visibility`: only pose landmarks set it. The script checks the protobuf `HasField('visibility')` flag: it was `True` for pose and `False` for face and both hands in both videos. Therefore only pose stores 4 fields; the other groups store 3.
- Face has 468 landmarks with `refine_face_landmarks=False` (478 if iris refinement is enabled; not used).
- Hand labels follow MediaPipe's left/right convention. In both clips the signer's dominant hand was reported as `right_hand`.
- In both sample clips the right hand is the dominant, active hand and the left hand is barely used ("tesekkurler": right hand to the chin/mouth, then outward; "merhaba": right hand near the face/chest). By the nature of these performances, the left hand is mostly absent from the frame or idle.

## 3. Per-frame Array Shape (Model Input Standard)

Total landmarks per frame: 33 + 468 + 21 + 21 = **543**.

Flattened feature vector per frame, concatenated in this fixed order:

```
[ pose (33x4 = 132) | face (468x3 = 1404) | left_hand (21x3 = 63) | right_hand (21x3 = 63) ]
= 1662 values
```

The script derives this size from the actual flattened arrays (not hard-coded); it was **1662** for both videos.

Model input standard:

- Per frame: `float32` vector of length **1662**, in the order above.
- Per sign sample: a sequence tensor of shape `[T, 1662]`, where `T` is the number of frames after resampling to the target frame rate (Section 4).
- Missing groups are filled as described in Section 6, so every frame always has exactly 1662 values.

Alternative compact variant: pose + hands only = 132 + 63 + 63 = **258** values per frame. The face mesh is 1404 of the 1662 values (84%). For TID, facial expression and mouthing carry grammatical information, so the full 1662 vector is the standard. A reduced face subset (e.g. lips, eyebrows, eyes) is a later optimisation to evaluate against model accuracy, not a decision made in this study.

## 4. Frame Rate Evaluation

Measured processing speed (video decode + Holistic inference, timed with `time.perf_counter`, CPU/XNNPACK on Apple M1):

| Video | Source FPS | Frames | Processing time | Processing FPS |
|---|---|---|---|---|
| `Ornek_Merhaba.mp4` | 25.00 | 150 | 4.97 s | **30.18** |
| `ornek_tesekkur.mp4` | 25.00 | 127 | 4.26 s | **29.81** |

Both runs processed frames faster than the 25 fps source rate on this machine. The input is only 324x216; higher-resolution camera input will add decode/resize cost, and the Holistic models run on a downscaled image internally either way. Speed on mobile devices was not measured in this study.

Recommendation:

- **Capture at 25-30 fps** (the samples are 25 fps). This keeps fast hand-shape transitions, which happen within a few frames, visible.
- **Process and store keypoints at 15 fps minimum, matching the project proposal's >=15 fps target.** 15 fps is the floor. Process every frame (25-30 fps) when the device keeps up, which it did here.
- For training data, resample every sequence to one fixed rate (proposed: 25 fps, matching the source data) so `T` is consistent across samples. 15 fps is the fallback rate for real-time inference on slower devices.
- Rationale: below about 15 fps, short handshape changes and movement endpoints get lost between frames. Above about 30 fps, the 1662-value vector grows the data volume linearly (25 fps x 1662 x 4 bytes is about 166 KB per second of raw float32) without adding sign information.

## 5. Noise Filtering and Smoothing

Observed in the runs (pose visibility threshold 0.5):

| Metric | merhaba | tesekkurler |
|---|---|---|
| Pose mean visibility (all 33) | 0.688 | 0.678 |
| Pose landmark-frames below 0.5 | 28.8% | 32.0% |
| Shoulders mean visibility | 0.999 / 1.000 | 1.000 / 1.000 |
| Elbows mean visibility (L / R) | 0.932 / 0.981 | 0.942 / 0.968 |
| Wrists mean visibility (L / R) | 0.763 / 0.849 | 0.829 / 0.873 |
| Wrists below 0.5 (L / R, % of frames) | 12.7% / 12.0% | 13.4% / 11.8% |

- The low overall pose visibility comes from the hip and leg landmarks (indices 23-32). The clips are framed at the waist, so these points are out of frame: their mean visibility was 0.169 (merhaba) and 0.074 (tesekkurler), versus 0.914 and 0.941 for landmarks 0-22. Upper-body landmarks are reliable.
- Low wrist visibility occurs mainly when the hands rest at the bottom edge of the frame before and after the sign.
- Jitter proxy (mean frame-to-frame wrist displacement of the hand landmarks, normalised image units): left hand 0.0399 / 0.0427, right hand 0.0288 / 0.0211 (merhaba / tesekkurler). This proxy mixes real signing motion with tracking noise, so these two clips cannot separate jitter from movement. A static-hand recording would be needed to measure pure jitter. This was **not measured** here.

Recommendation (applied in the preprocessing pipeline, in this order):

1. **Visibility gating:** treat pose landmarks with visibility < 0.5 as missing. Drop or ignore lower-body pose landmarks (23-32) for signing, since they are out of frame in typical signing footage.
2. **Gap filling:** apply the missing-data rule in Section 6.
3. **Light temporal smoothing:** keep Holistic's built-in `smooth_landmarks=True`. Optionally add a One Euro filter (or a short EMA) on hand landmarks. Tune it conservatively so fast handshape changes are not blurred. Validate it once the static-hand jitter test is recorded.
4. **Normalisation:** express coordinates relative to the body (e.g. centre on the shoulder midpoint and scale by shoulder width) so position and distance to the camera do not affect the model.

## 6. Missing Landmark Handling Rule

Observed missing rates (pose and face were detected in 100% of frames in both videos):

| Metric | merhaba | tesekkurler |
|---|---|---|
| left_hand missing | 125 / 150 frames (83.3%), longest gap 62 | 100 / 127 frames (78.7%), longest gap 70 |
| right_hand missing | 49 / 150 frames (32.7%), longest gap 25 | 20 / 127 frames (15.7%), longest gap 13 |
| No hand detected | 32.0% | 15.7% |
| At least one hand missing | 84.0% | 78.7% |

The frame-by-frame detection timeline shows two kinds of gaps:

- **Long gaps at the start/end of each clip**, when the hands are at rest below the frame (e.g. right hand not detected in the first 25 frames of merhaba and the first 13 frames of tesekkurler). These are real absences.
- **Short 1-3 frame dropouts of the active right hand in the middle of the sign** (most visible in merhaba), while the hand is close to the face/chest. These are detector failures.

The high left-hand missing rate (78.7-83.3%) is largely expected: the left hand is barely used in these two performances (Section 2), so its absence reflects the signing, not a detection failure. The handling rule below is still the same for both hands.

Rule:

1. **Short gaps (<= 5 frames at 25 fps, about 0.2 s): linear interpolation** between the last and next detection of that group.
2. **Longer gaps or gaps at the sequence start/end: zero-fill**, with no extrapolation.
3. **Presence mask:** append one binary flag per group (pose, face, left_hand, right_hand) per frame, set to 1 when the group was detected or interpolated and 0 when it was zero-filled. The model can then tell "hand absent" from "hand at coordinate 0". With the mask, the vector is 1662 + 4 = 1666 values; the 1662 keypoint block stays the standard.

Justification:

- **Not null/NaN:** neural networks and batching need fixed-shape numeric tensors; NaN breaks training.
- **Not zero-fill only:** zero-filling short dropouts creates sudden jumps to (0,0,0) mid-sign, which look like large fake motion. Interpolation removes these detector glitches.
- **Not interpolation only:** interpolating across long gaps (62-70 frames here) invents hand trajectories that never happened. Zero-fill plus the mask represents true absence honestly.

## 7. Feasibility Conclusion

**Verdict: feasible.** MediaPipe Holistic output is suitable as the model input for SignBridge-TR, with the preprocessing defined above.

- Setup works with a pinned legacy version (mediapipe 0.10.9) on Python 3.11.
- Output has a fixed, well-defined structure: 543 landmarks, 1662 values per frame.
- Pose and face were detected in 100% of frames. Shoulders and elbows are highly reliable (mean visibility >= 0.93).
- Processing ran at about 30 fps on an M1 laptop CPU, above the 25 fps source rate and the >=15 fps target.

Limitations observed:

- **Active-hand dropouts (main risk):** the dominant right hand was missing in 15.7-32.7% of frames, including short 1-3 frame dropouts in the middle of the sign. Part of the total is rest-pose frames at the clip start/end, when the hand is below the frame. The mid-sign dropouts are real detector failures. They are likely caused by the very low input resolution (324x216) and the hand coming close to the face/body. They should be re-tested with higher-resolution footage. Short-gap interpolation (Section 6) covers them in the meantime.
- **Non-dominant hand not meaningfully tested:** in both sample clips the right hand is dominant and the left hand is barely used. Its 78-83% absence reflects that it is hardly part of these signs, not a detection failure. Non-dominant-hand detection quality was therefore not measured here. It must be tested separately with footage that actively uses both hands.
- **Low resolution sample data:** both clips are 324x216. Hand landmarks are small at this size, so detection quality on real camera input (720p or higher) is expected to differ. This was not measured here.
- **Waist-up framing:** lower-body pose landmarks are unusable and should be excluded or ignored.
- **Jitter not isolated:** the two clips cannot separate tracking noise from signing motion (Section 5).
- **Small sample:** two short clips from two signers against a green background. This is not representative of real-world lighting, backgrounds or clothing.
- **Legacy API:** `mp.solutions.holistic` was removed from the newest mediapipe releases. The version pin must be kept, or the pipeline moved to the MediaPipe Tasks landmarkers (Pose, Hand and Face Landmarker) later. Their output format would need to be mapped to the same 1662-value layout.
- **Mobile performance not measured:** on-device speed on phones remains to be tested.

## 8. Sample Keypoint File

`docs/mediapipe_sample_keypoints.json` contains one real frame (frame index 33 of `Ornek_Merhaba.mp4`, the first frame where all four groups were detected). It includes:

- library versions and the concatenation order
- per-group landmark arrays (`pose` 33x4, `face` 468x3, `left_hand` 21x3, `right_hand` 21x3) with a `detected` flag
- the flattened 1662-value vector exactly as it would be fed to the model
