# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#z
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import sys

#avoid creating backup files
bpy.context.preferences.filepaths.save_version = 0

argv = sys.argv     
#argv = [
#   0:debug_mode
#   1:mark_objects, 
#   2:mark_materials, 
#   3:mark_poses, 
#   4:mark_worlds, # 
# ]

  
#argv = [
#   0:debug_mode
#   1:
# ]

argv = argv[argv.index("--") + 1:]  # get all args after "--"
debug = False
if argv[0] == 'True':
    debug = True
else:
    debug = False


def process_assets(argv):
    asset_type = argv[1].split()
    if not debug:
        print("asset_type: ", asset_type)    
    if 'object_mark' in asset_type:
        if debug:
            print('marking objects')
        for ob in bpy.data.objects:
            for i in bpy.data.scenes:  #only mark objects that are linked to a scene
                if ob.name in bpy.data.scenes[i.name].objects:
                    if ob.type == 'MESH':
                        mark_assets(ob)

    if 'object_clear' in asset_type:
        if debug:
            print('clearing objects')
        for ob in bpy.data.objects:
            clear_assets(ob)
        for me in bpy.data.meshes:
            clear_assets(me)

            
    if 'materials_mark' in asset_type:
        if debug:
            print('marking materials')
        for mat in bpy.data.materials:
            mark_assets(mat)    
    if 'materials_clear' in asset_type:
        if debug:
            print('clearing materials')
        for mat in bpy.data.materials:
            clear_assets(mat)

    """ 
    if 'poses_mark' in asset_type:
        if debug:
            print('marking poses')
        for pose in bpy.data.poses:
            mark_assets(pose)
    if 'poses_clear' in asset_type:
        if debug:
            print('clearing poses')
        for pose in bpy.data.poses:
            clear_assets(pose) 
    #"""

    """ 
    if 'worlds_mark' in asset_type:
        if debug: 
            print('marking worlds')
        for world in bpy.data.worlds:
            mark_assets(world)
    if 'worlds_clear' in asset_type:
        print('clearing worlds')
        for world in bpy.data.worlds:
            clear_assets(world)  
    #"""  

    #update all previews
    bpy.ops.wm.previews_ensure()

    #save the blend file to store asset marks
    bpy.ops.wm.save_mainfile()


def mark_assets(asset):
    if debug:
        print('    ', asset.name)
    asset.asset_mark()  
    #asset.asset_generate_preview()


def clear_assets(asset):
    if debug:
        print('    ', asset.name) 
    asset.asset_clear()
    asset.use_fake_user = True


process_assets(argv=argv)


'''
BLI_assert failed: C:\Repo\BlenderScripts\build_blender\BlenderGit\source\blender\windowmanager\intern\wm_window.c:2315, WM_opengl_context_create(), at 'BLI_thread_is_main()'

'''