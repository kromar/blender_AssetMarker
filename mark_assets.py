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

argv = sys.argv     #argguments = [mark_objects, mark_materials, mark_poses, mark_worlds]
print("argv: ", argv)
argv = argv[argv.index("--") + 1:]  # get all args after "--"
print("mark_assets.py: ", argv)




#Object 'name' can't be selected because it is not in View Layer 'Render Layer'!
""" for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type == 'FILE_BROWSER': """


def process_assets(argv):
    #bpy.ops.wm.previews_batch_clear()   

    if argv[0] == 'True': 
        print('marking objects')
        for ob in bpy.data.objects:
            for i in bpy.data.scenes:  #only mark objects that are linked to a scene
                if ob.name in bpy.data.scenes[i.name].objects:
                    if ob.type == 'MESH':
                        mark_assets(ob)
    else:
        print('clearing objects')
        for ob in bpy.data.objects:
            clear_assets(ob)
        for me in bpy.data.meshes:
            clear_assets(me)

    if argv[1] == 'True': 
        print('marking materials')
        for mat in bpy.data.materials:
            mark_assets(mat)
    else:
        print('clearing materials')
        for mat in bpy.data.materials:
            clear_assets(mat)

    """ if argv[2] == 'True': 
        print('marking poses')
        for pose in bpy.data.poses:
            mark_assets(pose)

    else:
        print('clearing poses')
        for pose in bpy.data.poses:
            clear_assets(pose) """

    """ if argv[3] == 'True': 
        print('marking worlds')
        for world in bpy.data.worlds:
            mark_assets(world)
    else:
        print('clearing worlds')
        for world in bpy.data.worlds:
            clear_assets(world)  """  

    #update all previews
    #bpy.ops.wm.previews_batch_generate()
    #bpy.ops.wm.previews_ensure()

    #save the blend file to store asset marks
    bpy.ops.wm.save_mainfile()


def mark_assets(asset):
    print('    ', asset.name)
    asset.asset_mark()  
    #asset.asset_generate_preview()


def clear_assets(asset):
    print('    ', asset.name) 
    asset.asset_clear()
    asset.use_fake_user = True

process_assets(argv=argv)


'''
BLI_assert failed: C:\Repo\BlenderScripts\build_blender\BlenderGit\source\blender\windowmanager\intern\wm_window.c:2315, WM_opengl_context_create(), at 'BLI_thread_is_main()'

'''