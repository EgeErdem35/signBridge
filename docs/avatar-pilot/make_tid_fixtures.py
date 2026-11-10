# SPDX-License-Identifier: GPL-3.0-or-later
"""Export hand-keyed approximations of two SIGN-HUB TİD reference sequences."""
from math import pi
from pathlib import Path
import runpy
import sys
from time import perf_counter

import bpy

OUTPUT = Path(__file__).resolve().parent
FIXTURES = ("tid-many", "tid-maternal-aunt")

def build_fixture(name):
    start = perf_counter()
    hand = runpy.run_path(str(OUTPUT / "make_fixtures.py"))
    rig, mesh = hand["rig"], hand["mesh"]
    scene = bpy.context.scene
    scene.render.fps = 24
    scene.frame_start, scene.frame_end = 1, 37
    rig.rotation_mode = "XYZ"

    # Establish face-relative coordinates without reproducing the reference signer.
    def marker(name, center, scale, color):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, location=center)
        obj = bpy.context.object
        obj.name = name
        obj.scale = scale
        material = bpy.data.materials.new(name)
        material.diffuse_color = (*color, 1)
        obj.data.materials.append(material)

    marker("Head", (0, 0, 2.45), (0.78, 0.53, 0.96), (0.42, 0.60, 0.65))
    marker("Nose", (0, -0.50, 2.48), (0.13, 0.14, 0.15), (0.50, 0.68, 0.70))
    marker("Shoulders", (0, 0.08, 0.35), (1.55, 0.53, 0.64), (0.25, 0.38, 0.46))
    rig.scale = (0.48,) * 3

    if name == "tid-many":
        from tid_many import poses
    else:
        from tid_maternal_aunt import poses
    for frame, location, wrist, base_angles, tip_angles, thumb in poses:
        rig.location = location
        rig.rotation_euler = (pi / 2, 0, wrist)
        rig.keyframe_insert(data_path="location", frame=frame)
        rig.keyframe_insert(data_path="rotation_euler", frame=frame)
        for finger, base, tip in zip(hand["FINGERS"], base_angles, tip_angles):
            for segment, angles in (("base", base), ("tip", (tip, 0, 0))):
                joint = rig.pose.bones[f"{finger}_{segment}"]
                joint.rotation_mode = "XYZ"
                joint.rotation_euler = angles
                joint.keyframe_insert(data_path="rotation_euler", frame=frame)
        joint = rig.pose.bones["thumb"]
        joint.rotation_mode = "XYZ"
        joint.rotation_euler = thumb
        joint.keyframe_insert(data_path="rotation_euler", frame=frame)
    rig.animation_data.action.name = name
    scene.frame_set(1)
    authored = perf_counter()
    bpy.ops.export_scene.gltf(
        filepath=str(OUTPUT / f"{name}.glb"),
        export_format="GLB",
        export_animation_mode="ACTIONS",
        export_frame_range=True,
        export_anim_slide_to_zero=True,
        export_frame_step=1,
    )
    print(f"{name}: scene and keyframes {authored - start:.3f}s; export {perf_counter() - authored:.3f}s", flush=True)


if __name__ == "__main__":
    sys.path.insert(0, str(OUTPUT))
    requested = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else list(FIXTURES)
    for fixture in requested:
        if fixture not in FIXTURES:
            raise ValueError(f"Unknown fixture: {fixture}")
        build_fixture(fixture)
