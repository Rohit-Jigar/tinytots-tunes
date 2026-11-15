import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from core.config import config
from core.logger import logger

class BlenderEngine:
    """
    Generates and executes Blender Python automation scripts for 3D/2.5D cartoon animation.
    Builds camera rigs, character keyframe animation, lighting, and stage geometry.
    """

    @classmethod
    def generate_blender_script(
        cls,
        image_path: str,
        output_video_path: str,
        duration_seconds: float,
        scene_title: str = "TinyTots Scene",
        character_name: str = "Barnaby Bear"
    ) -> str:
        """
        Generates a standalone Python script that can be executed directly inside Blender:
        `blender -b -P render_blender.py`
        """
        fps = config.VIDEO_FPS
        total_frames = int(duration_seconds * fps)
        safe_img_path = image_path.replace("\\", "/")
        safe_out_path = output_video_path.replace("\\", "/")

        script_content = f"""# ========================================================
# TinyTots Tunes - Automated Blender Animation Script
# Scene: {scene_title} | Character: {character_name}
# ========================================================
import bpy
import math

# 1. Clear existing objects
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.fps = {fps}
scene.frame_start = 1
scene.frame_end = {total_frames}
scene.render.resolution_x = {config.VIDEO_WIDTH}
scene.render.resolution_y = {config.VIDEO_HEIGHT}
scene.render.resolution_percentage = 100

# Set output format to FFmpeg MP4 H.264
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.filepath = '{safe_out_path}'

# 2. Setup Lighting (Bright Preschool Sunlight + Warm Fill)
sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
sun_data.energy = 4.0
sun_data.color = (1.0, 0.95, 0.85)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
scene.collection.objects.link(sun_obj)
sun_obj.location = (5.0, -8.0, 10.0)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-30))

# 3. Setup Camera with Animated Dolly & Gentle Bob
cam_data = bpy.data.cameras.new(name="PreschoolCam")
cam_data.lens = 50
cam_obj = bpy.data.objects.new(name="PreschoolCam", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

cam_obj.location = (0.0, -7.0, 1.2)
cam_obj.rotation_euler = (math.radians(82), 0, 0)

# Animate Camera slow zoom in
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.location = (0.0, -5.8, 1.25)
cam_obj.keyframe_insert(data_path="location", frame={total_frames})

# 4. Create Background Stage Plane with Textured Scene Illustration
bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 0.0, 1.0))
bg_plane = bpy.context.active_object
bg_plane.name = "BackgroundPlate"
# Scale to 16:9 ratio (width 7.1, height 4.0)
bg_plane.scale = (7.1, 4.0, 1.0)
bg_plane.rotation_euler = (math.radians(90), 0, 0)

mat_bg = bpy.data.materials.new(name="BackgroundMat")
mat_bg.use_nodes = True
nodes = mat_bg.node_tree.nodes
links = mat_bg.node_tree.links
bsdf = nodes.get("Principled BSDF")

# Image texture node
tex_node = nodes.new("ShaderNodeTexImage")
try:
    tex_image = bpy.data.images.load('{safe_img_path}')
    tex_node.image = tex_image
    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(tex_node.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 0.2
except Exception as e:
    print(f"Note: Could not load texture during script setup: {{e}}")

bg_plane.data.materials.append(mat_bg)

# 5. Add 3D Cartoon Star Props Floating with Keyframed Bounce
for i, x_pos in enumerate([-2.4, 2.4]):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.25, location=(x_pos, -0.5, 2.2))
    star = bpy.context.active_object
    star.name = f"Star_{{i}}"

    mat_star = bpy.data.materials.new(name=f"StarMat_{{i}}")
    mat_star.use_nodes = True
    star_nodes = mat_star.node_tree.nodes
    star_bsdf = star_nodes.get("Principled BSDF")
    star_bsdf.inputs["Base Color"].default_value = (1.0, 0.8, 0.1, 1.0)
    star_bsdf.inputs["Emission Color"].default_value = (1.0, 0.85, 0.2, 1.0)
    star_bsdf.inputs["Emission Strength"].default_value = 1.5
    star.data.materials.append(mat_star)

    # Animate bouncing and spinning
    for f in range(1, {total_frames} + 1, 15):
        star.location.z = 2.2 + 0.15 * math.sin(f * 0.2 + i)
        star.rotation_euler.z = f * 0.05
        star.keyframe_insert(data_path="location", frame=f)
        star.keyframe_insert(data_path="rotation_euler", frame=f)

print(f"Blender animation setup ready for {total_frames} frames.")
# bpy.ops.render.render(animation=True)
"""
        return script_content

    @classmethod
    def render_scene(
        cls,
        image_path: str,
        output_video_path: str,
        duration_seconds: float,
        scene_title: str = "TinyTots Scene"
    ) -> bool:
        """
        Executes headless Blender rendering if Blender is installed on system.
        Returns True if rendered via Blender, False otherwise.
        """
        script_content = cls.generate_blender_script(
            image_path=image_path,
            output_video_path=output_video_path,
            duration_seconds=duration_seconds,
            scene_title=scene_title
        )

        script_path = Path(output_video_path).parent / f"blender_{Path(output_video_path).stem}.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        blender_bin = config.BLENDER_PATH
        if not blender_bin:
            logger.info("Blender path not configured. Exported Blender Python animation script to %s", script_path)
            return False

        if not os.path.exists(blender_bin):
            logger.warning("Blender binary not found at %s. Exported script to %s", blender_bin, script_path)
            return False

        try:
            logger.info("Invoking headless Blender render: %s...", script_path)
            cmd = [blender_bin, "-b", "-P", str(script_path)]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
            return os.path.exists(output_video_path)
        except Exception as e:
            logger.warning("Blender rendering execution encountered an error: %s", e)
            return False

blender_engine = BlenderEngine()

