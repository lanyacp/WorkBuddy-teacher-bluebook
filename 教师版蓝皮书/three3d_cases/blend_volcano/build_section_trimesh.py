# -*- coding: utf-8 -*-
"""
路线 C 对照实操：不装 Blender 也能建出「剖面 + 多地层 + 内部腔体」教学模型。
产出 GLB（含 PBR 材质），供课堂旋转观察。

与 Blender 路线的差异：这是纯几何建模，适合规则形体与教学示意；
不规则地形、真实贴图、关键帧动画仍需 Blender。
"""
import os
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

OUT = r"D:/projects/WorkBuddy/2026-06-17-11-18-20/教师版蓝皮书/three3d_cases/blend_volcano"
os.makedirs(OUT, exist_ok=True)


# ---------- 基础几何 ----------
def frustum(r_bot, r_top, height, sections=64):
    """圆台（锥台）：底面半径 r_bot、顶面半径 r_top、高 height，中心在原点，向上生长"""
    ang = np.linspace(0, 2 * np.pi, sections, endpoint=False)
    bot = np.column_stack([r_bot * np.cos(ang), r_bot * np.sin(ang), np.zeros(sections)])
    top = np.column_stack([r_top * np.cos(ang), r_top * np.sin(ang), np.full(sections, height)])
    bot_c = np.array([[0.0, 0.0, 0.0]])
    top_c = np.array([[0.0, 0.0, height]])
    v = np.vstack([bot, top, bot_c, top_c])
    bi, ti = 2 * sections, 2 * sections + 1
    faces = []
    for i in range(sections):
        j = (i + 1) % sections
        faces.append([i, j, sections + j])
        faces.append([i, sections + j, sections + i])
        faces.append([bi, j, i])
        faces.append([ti, sections + i, sections + j])
    return trimesh.Trimesh(vertices=v, faces=np.array(faces), process=True)


def cut_front(mesh):
    """剖面切割：切掉 y > 0 的前半，露出内部（保 y <= 0）"""
    try:
        return mesh.slice_plane(plane_origin=[0, 0, 0], plane_normal=[0, -1, 0], cap=True)
    except Exception as e:
        print("  [warn] 切割失败，保留原形:", e)
        return mesh


def mat(rgba, rough=0.85, metal=0.0, emit=None, emit_s=0.0):
    """返回 (PBRMaterial, 顶点颜色数组) —— 顶点颜色是 GLB 导出时真正可靠的颜色来源"""
    color_u8 = tuple(int(c * 255) for c in rgba[:3]) + (int(rgba[3] * 255) if len(rgba) > 3 else 255,)
    kw = dict(baseColorFactor=list(rgba), roughnessFactor=rough, metallicFactor=metal)
    if emit is not None:
        kw["emissiveFactor"] = list(emit)
    return PBRMaterial(**kw), color_u8


# ---------- 场景 ----------
scene = trimesh.Scene()


def add(name, mesh, mat_tuple):
    material, color_u8 = mat_tuple
    mesh = cut_front(mesh)   # 先切割（切割会重建 mesh 丢失 visual）
    # 切割后再设顶点颜色——这是 GLB 导出时真正生效的颜色通道
    n = len(mesh.vertices)
    vcol = np.tile(np.array(color_u8, dtype=np.uint8), (n, 1))
    mesh.visual = trimesh.visual.ColorVisuals(vertex_colors=vcol)
    mesh.visual.material = material   # PBR 材质作补充
    scene.add_geometry(mesh, node_name=name, geom_name=name)
    print("  +", name, "顶点", len(mesh.vertices), "颜色", color_u8)


print("[1/4] 建地面与五层地层…")
# 地面圆盘
ground = trimesh.creation.cylinder(radius=9.0, height=0.5, sections=64)
ground.apply_translation([0, 0, -0.25])
add("Ground", ground, mat((0.36, 0.33, 0.30, 1), rough=0.95))

# 五层地层（圆台堆叠，半径逐层收小）
layers = [
    ("Layer1_topsoil",  5.2, 4.6, 1.0, 0.0,  (0.45, 0.31, 0.20, 1)),
    ("Layer2_sediment", 4.6, 3.9, 1.1, 1.0,  (0.55, 0.42, 0.30, 1)),
    ("Layer3_andesite", 3.9, 3.1, 1.2, 2.1,  (0.42, 0.42, 0.45, 1)),
    ("Layer4_basalt",   3.1, 2.3, 1.2, 3.3,  (0.22, 0.22, 0.26, 1)),
    ("Layer5_deep",     2.3, 1.5, 1.3, 4.5,  (0.15, 0.13, 0.16, 1)),
]
for name, rb, rt, h, z, color in layers:
    m = frustum(rb, rt, h)
    m.apply_translation([0, 0, z])
    add(name, m, mat(color, rough=0.9))

print("[2/4] 建火山锥、火山口…")
cone = frustum(1.5, 0.85, 1.4)
cone.apply_translation([0, 0, 5.8])
add("VolcanoCone", cone, mat((0.15, 0.13, 0.16, 1), rough=0.88))

crater = trimesh.creation.cylinder(radius=0.85, height=0.25, sections=48)
crater.apply_translation([0, 0, 7.3])
add("Crater", crater, mat((0.30, 0.26, 0.24, 1), rough=0.92))

print("[3/4] 建岩浆房与通道…")
# 岩浆房（略扁椭球，放大并上移到剖面可见位置）
chamber = trimesh.creation.icosphere(subdivisions=3, radius=1.65)
chamber.apply_scale([1.35, 1.35, 0.75])
chamber.apply_translation([0, 0, 1.6])
add("MagmaChamber", chamber,
    mat((0.95, 0.30, 0.06, 1), rough=0.5, emit=(1.0, 0.32, 0.05)))

# 主通道（从岩浆房顶部直通火山口）
main = trimesh.creation.cylinder(radius=0.45, height=5.8, sections=32)
main.apply_translation([0, 0, 4.3])
add("MainConduit", main,
    mat((0.98, 0.42, 0.10, 1), rough=0.55, emit=(1.0, 0.45, 0.12)))

# 侧通道（在 xz 平面内斜向山腰，正好被剖面切成两半，截面可见）
side = trimesh.creation.cylinder(radius=0.28, height=3.2, sections=24)
rot = trimesh.transformations.rotation_matrix(np.radians(65), [0, 1, 0])
side.apply_transform(rot)
side.apply_translation([1.9, 0.0, 3.2])
add("SideConduit", side,
    mat((0.98, 0.42, 0.10, 1), rough=0.55, emit=(1.0, 0.45, 0.12)))

print("[4/4] 导出 GLB…")
glb = os.path.join(OUT, "volcano_section.glb")
scene.export(glb)
size = os.path.getsize(glb)
print("[+] 导出:", glb, "%.2f MB" % (size / 1024 / 1024))

# 汇总
total_v = sum(len(g.vertices) for g in scene.geometry.values())
print("[+] 对象数:", len(scene.geometry), "顶点总数:", total_v)
print("[+] 对象名:", list(scene.geometry.keys()))
print("DONE")
