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
argv = argv[argv.index("--") + 1:]  # get all args after "--"

#print(argv[0], argv[1])

# 0 = objects
# 1 = materials
# 2 = meshes
# 3 = textures

#Object 'CysticArtery.001' can't be selected because it is not in View Layer 'Render Layer'!

for v in bpy.data.objects:
    v.select_set(True)
    if argv[0] == 'True': 
        v.asset_mark()
    else:
        v.asset_clear()

try:
    for v in bpy.data.materials:
        if argv[1] == 'True': 
            v.asset_mark()
        else:
            v.asset_clear()
except:
    pass
 
try:    
    for v in bpy.data.meshes:
        if argv[2] == 'True': 
            v.asset_mark()
        else:
            v.asset_clear()
except:
    pass           

try:
    for v in bpy.data.textures:
        if argv[3] == 'True': 
            v.asset_mark()
        else:
            v.asset_clear()
except:
    pass





#save the blend file to store asset marks
bpy.ops.wm.save_mainfile()