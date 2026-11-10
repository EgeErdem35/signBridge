# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate two original, non-linguistic hand motion fixtures with Blender 4.5."""
from pathlib import Path

import bpy

OUTPUT = Path(__file__).resolve().parent
FINGERS = ("index", "middle", "ring", "little")

bpy.ops.wm.read_factory_settings(use_empty=True)
skeleton = bpy.data.armatures.new("SyntheticHandSkeleton")
rig = bpy.data.objects.new("SyntheticHand", skeleton)
bpy.context.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
rig.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")

palm = skeleton.edit_bones.new("palm")
palm.head = (0, 0, 0)
palm.tail = (0, 0.85, 0)
for index, (name, length) in enumerate(zip(FINGERS, (0.48, 0.56, 0.51, 0.39))):
    x = -0.39 + index * 0.26
    base = skeleton.edit_bones.new(f"{name}_base")
    base.head = (x, 0.85, 0)
    base.tail = (x, 0.85 + length, 0)
    base.parent = palm
    tip = skeleton.edit_bones.new(f"{name}_tip")
    tip.head = base.tail
    tip.tail = (x, 0.85 + length * 1.7, 0)
    tip.parent = base
    tip.use_connect = True
thumb = skeleton.edit_bones.new("thumb")
thumb.head = (-0.49, 0.31, 0)
thumb.tail = (-0.81, 0.64, 0)
thumb.parent = palm
bpy.ops.object.mode_set(mode="OBJECT")

material = bpy.data.materials.new("Hand teal")
material.diffuse_color = (0.08, 0.58, 0.52, 1.0)

parts = []
for bone in skeleton.bones:
    center = (bone.head_local + bone.tail_local) / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    part = bpy.context.object
    part.rotation_euler = bone.matrix_local.to_euler()
    if bone.name == "palm":
        part.dimensions = (1.04, 0.83, 0.23)
    else:
        part.dimensions = (0.18, bone.length * 0.88, 0.17)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = part.modifiers.new("Round edges", "BEVEL")
    bevel.width = 0.045
    bevel.segments = 1
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    part.data.materials.append(material)
    part.vertex_groups.new(name=bone.name).add(
        list(range(len(part.data.vertices))), 1.0, "REPLACE"
    )
    parts.append(part)

bpy.ops.object.select_all(action="DESELECT")
for part in parts:
    part.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
mesh = bpy.context.object
mesh.name = "SyntheticHandMesh"
mesh.parent = rig
skin = mesh.modifiers.new("Hand skin", "ARMATURE")
skin.object = rig

if __name__ == "__main__":
    scene = bpy.context.scene
    scene.render.fps = 24
    scene.frame_start, scene.frame_end = 1, 49
    for fixture, fingers in (("index-curl", ("index",)), ("four-finger-curl", FINGERS)):
        rig.animation_data_clear()
        for action in list(bpy.data.actions):
            bpy.data.actions.remove(action)
        for name in FINGERS:
            for segment, angle in (("base", -1.05), ("tip", -0.75)):
                joint = rig.pose.bones[f"{name}_{segment}"]
                joint.rotation_mode = "XYZ"
                for frame in (1, 25, 49):
                    joint.rotation_euler.x = angle if frame == 25 and name in fingers else 0
                    joint.keyframe_insert(data_path="rotation_euler", frame=frame)
        rig.animation_data.action.name = fixture
        scene.frame_set(1)
        bpy.ops.export_scene.gltf(
            filepath=str(OUTPUT / f"{fixture}.glb"),
            export_format="GLB",
            export_animation_mode="ACTIONS",
            export_frame_range=True,
            export_anim_slide_to_zero=True,
            export_frame_step=1,
        )
