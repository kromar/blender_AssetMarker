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


bpy.ops.wm.previews_batch_clear()


if argv[0] == 'True': 
    print('marking objects')
    for v in bpy.data.objects:
        for i in bpy.data.scenes:  #only mark objects that are linked to a scene
            if v.name in bpy.data.scenes[i.name].objects:
                if v.type == 'MESH':
                    print('    3 ', v.name)
                    v.asset_mark()  
                    v.asset_generate_preview()

else:
    print('clearing objects')
    for v in bpy.data.objects:
        print('    ', v.name) 
        v.asset_clear() 
        v.use_fake_user = True

    for v in bpy.data.meshes:
        print('    ', v.name) 
        v.asset_clear()
        v.use_fake_user = True


if argv[1] == 'True': 
    print('marking materials')
    for v in bpy.data.materials:
        print('    ', v.name)
        v.asset_mark()  
        v.asset_generate_preview()

else:
    print('clearing materials')
    for v in bpy.data.materials:
        print('    ', v.name) 
        v.asset_clear()
        v.use_fake_user = True


""" if argv[2] == 'True': 
    print('marking poses')
    for v in bpy.data.poses:
        print('    ', v.name)
        v.asset_mark()  
        v.asset_generate_preview()

else:
    print('clearing poses')
    for v in bpy.data.poses:
        print('    ', v.name) 
        v.asset_clear()
        v.use_fake_user = True """


if argv[3] == 'True': 
    print('marking worlds')
    for v in bpy.data.worlds:
        print('    ', v.name)
        v.asset_mark()  
        v.asset_generate_preview()

else:
    print('clearing worlds')
    for v in bpy.data.worlds:
        print('    ', v.name) 
        v.asset_clear()
        v.use_fake_user = True

""" 
for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type == 'FILE_BROWSER':  
            for v in bpy.data.objects:
                v.select_set(True)
                bpy.ops.ed.lib_id_generate_preview()
                
                v.select_set(False) """

#update all previews
#bpy.ops.wm.previews_batch_generate()
bpy.ops.wm.previews_ensure()

#save the blend file to store asset marks
bpy.ops.wm.save_mainfile()
bpy.ops.wm.quit_blender()