# -*- coding: utf-8 -*-
"""
在 Blender 里正确打开 GLB —— 一键脚本

为什么需要它：
  Blender 的「文件 > 打开」(Ctrl+O) 只认 .blend，GLB 根本不会显示在对话框里。
  GLB 必须走「文件 > 导入 > glTF 2.0」，而且 Blender 默认场景里那个 2 米大的
  立方体会把 1 米左右的模型整个包住，看起来就像「什么都没导入」。

它做的事：
  1. 清空默认场景（Cube / Camera / Light 全删）
  2. 导入 GLB / glTF
  3. 按模型实际大小自动摆好相机和灯光
  4. 视口切到材质预览，直接看到彩色模型
  5. 自动框住模型，不用再按 Home 键

用法（二选一）：
  A. 把 GLB 文件拖到 用Blender打开模型.bat 图标上
  B. 双击 用Blender打开模型.bat，按提示输入编号
"""

import bpy
import sys
import os
import math
import mathutils


# ---------- 工具函数 ----------

def clean_scene():
    """清空默认场景里的所有对象。
    这是最关键的一步 —— 不清空的话，2m 的 Cube 会把 1m 的模型包在里面。"""
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # 顺手清掉残留的孤立数据块
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def world_bounds():
    """算出所有网格在世界坐标下的联合包围盒。"""
    mn = mathutils.Vector((1e18, 1e18, 1e18))
    mx = mathutils.Vector((-1e18, -1e18, -1e18))
    found = False
    for o in bpy.context.scene.objects:
        if o.type != 'MESH':
            continue
        found = True
        for corner in o.bound_box:
            w = o.matrix_world @ mathutils.Vector(corner)
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    if not found:
        return None, None
    return mn, mx


def setup_camera_and_light(mn, mx):
    """按包围盒大小自动摆相机和灯，保证一打开就看得到模型。"""
    center = (mn + mx) / 2.0
    size = mx - mn
    diag = max(size.length, 0.5)

    # --- 相机：右前上方 45°，距离按对角线算 ---
    cam_data = bpy.data.cameras.new('AutoCam')
    cam_data.lens = 50
    cam_data.clip_start = max(diag * 0.001, 0.001)
    cam_data.clip_end = diag * 100
    cam = bpy.data.objects.new('AutoCam', cam_data)
    bpy.context.scene.collection.objects.link(cam)

    dist = diag * 1.75
    cam.location = center + mathutils.Vector((dist * 0.62, -dist * 0.72, dist * 0.42))
    direction = center - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam

    # --- 补光：一盏 Sun + 偏冷的世界环境光 ---
    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new('World')
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        # 世界亮度别压太低，否则切到渲染模式整片发黑
        bg.inputs[0].default_value = (0.11, 0.12, 0.15, 1.0)
        bg.inputs[1].default_value = 2.0

    sun_data = bpy.data.lights.new('KeyLight', 'SUN')
    sun_data.energy = 4.2
    sun_data.angle = math.radians(12)
    sun = bpy.data.objects.new('KeyLight', sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.location = center + mathutils.Vector((diag, -diag * 0.9, diag * 1.1))
    sun.rotation_euler = (math.radians(50), 0, math.radians(35))

    # 补光：从另一侧打亮暗部，避免背光面糊成一团黑
    fill_data = bpy.data.lights.new('FillLight', 'AREA')
    fill_data.energy = diag * diag * 28
    fill_data.size = diag * 1.8
    fill = bpy.data.objects.new('FillLight', fill_data)
    bpy.context.scene.collection.objects.link(fill)
    fill.location = center + mathutils.Vector((-diag * 1.0, -diag * 0.55, diag * 0.55))
    fill.rotation_euler = (center - fill.location).to_track_quat('-Z', 'Y').to_euler()

    return cam, diag


def polish_viewport():
    """视口切成材质预览，自动框住模型，这样不用手动找模型跑哪去了。"""
    # 只选中网格，后面 view_selected 就能精准框住模型（不会把灯和相机算进去）
    bpy.ops.object.select_all(action='DESELECT')
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in meshes:
        o.select_set(True)
    if meshes:
        bpy.context.view_layer.objects.active = meshes[0]

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            space = area.spaces.active
            # 材质预览：能看到 GLB 自带的颜色和贴图，而不是一片灰
            try:
                space.shading.type = 'MATERIAL'
                # 关键：不要沿用场景世界。用 Blender 内置的棚拍 HDRI，
                # 亮度均匀、不用布光就能看清贴图；勾上场景世界反而会把模型压暗。
                space.shading.use_scene_world = False
                space.shading.use_scene_lights = False
                # 材质预览偶尔会被上一份文件残留的曝光值拖暗，顺手归位
                space.shading.studiolight_intensity = 1.0
            except Exception:
                pass
            # 框住选中的模型
            regions = [r for r in area.regions if r.type == 'WINDOW']
            if regions:
                try:
                    with bpy.context.temp_override(window=window, area=area, region=regions[0]):
                        bpy.ops.view3d.view_selected(use_all_regions=False)
                except Exception:
                    pass


# ---------- 主流程 ----------

def main():
    # 取出命令行里 -- 之后的文件路径
    argv = sys.argv
    paths = []
    if '--' in argv:
        paths = argv[argv.index('--') + 1:]
    paths = [p for p in paths
             if os.path.isfile(p) and p.lower().endswith(('.glb', '.gltf'))]

    if not paths:
        print('[GLB] 没收到有效的 GLB 文件路径。')
        print('[GLB] 用法：把 .glb 文件拖到 bat 图标上，或双击 bat 后输入编号。')
        return

    clean_scene()

    imported = []
    for p in paths:
        try:
            bpy.ops.import_scene.gltf(filepath=p)
            imported.append(p)
            print('[GLB] 已导入: %s' % os.path.basename(p))
        except Exception as e:
            print('[GLB] 导入失败 %s -> %s: %s' % (p, type(e).__name__, e))

    if not imported:
        return

    mn, mx = world_bounds()
    if mn is None:
        print('[GLB] 导入成功，但里面没有网格对象。')
        return

    cam, diag = setup_camera_and_light(mn, mx)
    polish_viewport()

    size = mx - mn
    tris = sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type == 'MESH')
    n_mesh = len([o for o in bpy.context.scene.objects if o.type == 'MESH'])

    print('=' * 56)
    print('[GLB] 导入完成')
    print('      模型尺寸: %.2f x %.2f x %.2f' % tuple(size))
    print('      网格数: %d   面数: %d' % (n_mesh, tris))
    print('      已自动摆好相机和灯光，视口切到材质预览')
    print('      小技巧：选中模型按 小键盘句号(.) 可随时聚焦')
    print('      数字键 1/3/7 = 前视/侧视/顶视，5 = 透视切换')
    print('=' * 56)

    # 写日志：出问题时把这行记录发出来就能定位
    try:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '_open_glb_last.log')
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('Blender %s\n' % bpy.app.version_string)
            for p in imported:
                f.write('文件: %s\n' % p)
                f.write('  体积: %.1f MB\n' % (os.path.getsize(p) / 1048576.0))
            f.write('尺寸: %.2f x %.2f x %.2f\n' % tuple(size))
            f.write('网格数: %d  面数: %d\n' % (n_mesh, tris))
            f.write('结果: OK\n')
    except Exception:
        pass


main()
