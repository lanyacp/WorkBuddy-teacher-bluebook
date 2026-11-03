# -*- coding: utf-8 -*-
"""
路线 C 实操：Blender 无头脚本建「火山剖面」教学模型
体现路线 C 独有能力：剖面结构 + 不规则地形 + 多地层 + 内部腔体

用法：blender -b -P volcano_section.py -- <输出目录>
"""
import bpy
import math
import os
import sys

# ---------- 0. 取输出目录 ----------
argv = sys.argv
out_dir = r"D:/projects/WorkBuddy/2026-06-17-11-18-20/教师版蓝皮书/three3d_cases/blend_volcano"
if "--" in argv:
    idx = argv.index("--")
    if idx + 1 < len(argv):
        out_dir = argv[idx + 1]
os.makedirs(out_dir, exist_ok=True)

print("[1/8] 输出目录:", out_dir)


# ---------- 1. 清空场景 ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


# ---------- 2. 材质工具 ----------
def make_mat(name, color, rough=0.75, emit=None, emit_strength=0.0, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if emit is not None:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emit_strength
    return mat


MAT_GROUND = make_mat("ground", (0.36, 0.33, 0.30), rough=0.95)
# 地层从外到内、从上到下
MAT_L1 = make_mat("layer_topsoil", (0.45, 0.31, 0.20), rough=0.9)   # 表土
MAT_L2 = make_mat("layer_sediment", (0.55, 0.42, 0.30), rough=0.9)  # 沉积层
MAT_L3 = make_mat("layer_andesite", (0.42, 0.42, 0.45), rough=0.85) # 安山岩
MAT_L4 = make_mat("layer_basalt", (0.22, 0.22, 0.26), rough=0.8)    # 玄武岩
MAT_L5 = make_mat("layer_deep", (0.15, 0.13, 0.16), rough=0.8)      # 深部岩体
MAT_MAGMA = make_mat("magma", (0.95, 0.30, 0.06), rough=0.5,
                     emit=(1.0, 0.32, 0.05), emit_strength=3.0)
MAT_CONDUIT = make_mat("conduit", (0.98, 0.42, 0.10), rough=0.55,
                       emit=(1.0, 0.45, 0.12), emit_strength=1.6)
MAT_CRATER = make_mat("crater", (0.30, 0.26, 0.24), rough=0.9)
print("[2/8] 材质就绪")


# ---------- 3. 地面 ----------
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=9.0, depth=0.5, location=(0, 0, -0.25))
ground = bpy.context.active_object
ground.name = "Ground"
ground.data.materials.append(MAT_GROUND)


# ---------- 4. 分层地层（每层是一个圆盘/圆台，堆叠成火山体） ----------
# (名字, 底部半径, 顶部半径, 高度, z中心, 材质)
layers = [
    ("Layer1_topsoil",   5.2, 4.6, 1.0, 0.5,  MAT_L1),
    ("Layer2_sediment",  4.6, 3.9, 1.1, 1.55, MAT_L2),
    ("Layer3_andesite",  3.9, 3.1, 1.2, 2.7,  MAT_L3),
    ("Layer4_basalt",    3.1, 2.3, 1.2, 3.9,  MAT_L4),
    ("Layer5_deep",      2.3, 1.5, 1.3, 5.15, MAT_L5),
]
for name, r_bot, r_top, h, z, mat in layers:
    bpy.ops.mesh.primitive_cone_add(
        vertices=64, radius1=r_bot, radius2=r_top,
        depth=h, location=(0, 0, z))
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
print("[3/8] 五层地层堆叠完成")


# ---------- 5. 火山锥顶 + 火山口 ----------
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=1.5, radius2=0.85,
                                depth=1.4, location=(0, 0, 6.5))
cone = bpy.context.active_object
cone.name = "VolcanoCone"
cone.data.materials.append(MAT_L5)
bpy.ops.object.shade_smooth()

# 火山口：一个略小的深色圆盘盖住顶端
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.85, depth=0.25,
                                    location=(0, 0, 7.15))
crater = bpy.context.active_object
crater.name = "Crater"
crater.data.materials.append(MAT_CRATER)
print("[4/8] 火山锥与火山口完成")


# ---------- 6. 岩浆房 + 主通道 + 侧通道 ----------
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24,
                                     radius=1.35, location=(0, 0, 1.0))
chamber = bpy.context.active_object
chamber.name = "MagmaChamber"
chamber.scale = (1.25, 1.25, 0.85)   # 略扁，更像岩浆房
chamber.data.materials.append(MAT_MAGMA)
bpy.ops.object.shade_smooth()

# 主通道：从岩浆房直通火山口
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.42, depth=6.4,
                                    location=(0, 0, 4.0))
main = bpy.context.active_object
main.name = "MainConduit"
main.data.materials.append(MAT_CONDUIT)
bpy.ops.object.shade_smooth()

# 侧通道：斜着通向山腰
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.28, depth=3.2,
                                    location=(1.75, 0.9, 3.1))
side = bpy.context.active_object
side.name = "SideConduit"
side.rotation_euler = (0.0, math.radians(58), math.radians(28))
side.data.materials.append(MAT_CONDUIT)
bpy.ops.object.shade_smooth()
print("[5/8] 岩浆房与通道完成")


# ---------- 7. 剖面：布尔切掉 y>0 的前半，露出内部 ----------
bpy.ops.mesh.primitive_cube_add(size=24, location=(0, 12, 3))
cutter = bpy.context.active_object
cutter.name = "Cutter"

for target_name in ["Ground"] + [l[0] for l in layers] + \
                   ["VolcanoCone", "Crater", "MagmaChamber", "MainConduit", "SideConduit"]:
    obj = bpy.data.objects.get(target_name)
    if obj is None:
        continue
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="SectionCut", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    mod.solver = 'EXACT'
    # 应用修改器
    bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.data.objects.remove(cutter, do_unlink=True)
print("[6/8] 剖面切割完成（前半已切掉，露出地层与岩浆房）")


# ---------- 8. 灯光 + 相机 ----------
bpy.ops.object.light_add(type='SUN', location=(6, -6, 12))
sun = bpy.context.active_object
sun.data.energy = 3.2
sun.rotation_euler = (math.radians(48), 0, math.radians(38))

bpy.ops.object.light_add(type='AREA', location=(-7, -5, 7))
fill = bpy.context.active_object
fill.data.energy = 420
fill.data.size = 8
fill.rotation_euler = (math.radians(55), 0, math.radians(-42))

bpy.ops.object.camera_add(location=(11.5, -12.5, 8.6))
cam = bpy.context.active_object
cam.name = "ClassroomCamera"
cam.rotation_euler = (math.radians(64), 0, math.radians(42))
cam.data.lens = 42
scene.camera = cam
print("[7/8] 灯光与相机就位")


# ---------- 9. 渲染设置 + 渲染 PNG ----------
scene.render.engine = 'BLENDER_EEVEE'  # Blender 5.x 的 EEVEE 名称
scene.render.resolution_x = 1280
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.86, 0.90, 0.95, 1.0)   # 浅色背景，投影友好
bg.inputs[1].default_value = 1.0

png_path = os.path.join(out_dir, "volcano_section.png")
scene.render.filepath = png_path
bpy.ops.render.render(write_still=True)
print("[8/8] 渲染完成:", png_path)


# ---------- 10. 导出 GLB ----------
glb_path = os.path.join(out_dir, "volcano_section_blender.glb")
bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                          export_apply=True, export_yup=False)  # 保持 Z-up，不做坐标转换
print("[+] GLB 导出:", glb_path)

# 统计
verts = sum(len(o.data.vertices) for o in bpy.data.objects if o.type == 'MESH')
print("[+] 场景对象:", [o.name for o in bpy.data.objects])
print("[+] 顶点总数:", verts)
print("DONE")
