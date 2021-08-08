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

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

print(argv[0], argv[1])

# 0 = objects
# 1 = materials

if argv[1] == 'False':  
    state = False
else:
    state = True



if argv[0] == 'objects':
    for ob in bpy.data.objects:
        ob.select_set(True)
        if state:
            ob.asset_mark()
        else:
            ob.asset_clear()



if argv[0] == 'objects':
    for ob in bpy.data.objects:
        ob.select_set(True)
        if state:
            ob.asset_mark()
        else:
            ob.asset_clear()

if argv[0] == 'meshes':
    for ob in bpy.data.meshes:
        if state:
            ob.asset_mark()
        else:
            ob.asset_clear()

if argv[0] == 'materials':
    for ob in bpy.data.materials:
        if state:
            ob.asset_mark()
        else:
            ob.asset_clear()
            
if argv[0] == 'textures':
    for ob in bpy.data.textures:
        if state:
            ob.asset_mark()
        else:
            ob.asset_clear()


#save the blend file to store asset marks
bpy.ops.wm.save_mainfile()