
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
# 

import bpy
import sys


#avoid creating backup files
bpy.context.preferences.filepaths.save_version = 0

argv = sys.argv  
#argv = [
#   0:debug_mode
#   2:asset_type
#   1:asset_name
# ]

argv = argv[argv.index("--") + 1:]  # get all args after "--"
debug = True

if argv[0] == 'True':
    debug = True
    print(argv)
else:
    debug = False


def process_assets(argv):

    asset_type = argv[1]
    asset_name = argv[2]
    
    if debug:     
        print("asset_type: ", asset_type)
        print("asset: ",    asset_name)   

    #find asset by asset type and clear the mark
    if asset_type in ('MESH', 'SURFACE', 'META', 'CURVE'):
        clear_assets(bpy.data.objects[asset_name])

    if asset_type == 'MATERIAL':
        clear_assets(bpy.data.materials[asset_name])
            
    if asset_type == 'COLLECTION':
        clear_assets(bpy.data.collections[asset_name])

    if asset_type == 'LIGHT':
        clear_assets(bpy.data.lights[asset_name])

    if asset_type == 'NODETREE':
        clear_assets(bpy.data.node_groups[asset_name])

    if asset_type == 'CAMERA':
        clear_assets(bpy.data.cameras[asset_name])


    #save the blend file to store asset marks
    print('save_mainfile')
    bpy.ops.wm.save_mainfile()
    

def clear_assets(asset):
    print('    Clear Asset: ', asset.name) 
    asset.asset_clear()
    asset.use_fake_user = True

    
process_assets(argv=argv)