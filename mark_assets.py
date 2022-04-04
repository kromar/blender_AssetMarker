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
'''
argv = [
    0:debug_mode
    1:asset_type
    2:blend source
    3:asset_list
]
'''

argv = argv[argv.index("--") + 1:]  # get all args after "--"
debug = True
if argv[0] == 'True':
    debug = True
    print(argv)
else:
    debug = False

def paste_asset(): 
    #paste from buffer 
    print("APPEND ASSETS")  
    
    '''
    https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html
    '''

    # path to the blend
    filepath = argv[2]
    print("FILEPATH: ", filepath)   
    # name of collection(s) to append or link
    #coll_name = "MyCollection"   
    # name of object(s) to append or link
    if argv[3]:
        assets = argv[3].split()
        for asset in assets:
            obj_name = asset
            print("arrived assset: ", asset)

    '''    
    # link all collections starting with 'MyCollection'
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
    # link collection to scene collection
    for coll in data_to.collections:
        if coll is not None:
            bpy.context.scene.collection.children.link(coll)
    '''
    
    """ 
    # link all objects starting with 'Cube'
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name.startswith(obj_name)]
    #link object to current scene
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj) # Blender 2.8x
    
    """
def delete_asset(asset):
    pass

def process_assets(argv):
    #bpy.ops.wm.previews_clear()
    #bpy.ops.wm.previews_batch_clear()
    asset_type = argv[1].split()
    if not debug:
        print("asset_type: ", asset_type)    
    if 'mark_object' in asset_type:
        for ob in bpy.data.objects:
            for i in bpy.data.scenes:  #only mark objects that are linked to a scene
                if ob.name in bpy.data.scenes[i.name].objects:
                    
                    if ob.type == 'MESH':
                        if 'mark_mesh' in asset_type:
                            mark_assets(ob)
                        if 'clear_mesh' in asset_type:
                            clear_assets(ob)

                    if ob.type == 'SURFACE':
                        if 'mark_surface' in asset_type:
                            mark_assets(ob)
                        if 'clear_surface' in asset_type:
                            clear_assets(ob)
                    
                    if ob.type == 'META':
                        if 'mark_meta' in asset_type:
                            mark_assets(ob)
                        if 'clear_meta' in asset_type:
                            clear_assets(ob)

                    if ob.type == 'CURVE':    
                        if 'mark_curve' in asset_type:
                            mark_assets(ob)
                        if 'clear_curve' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'FONT':
                        if 'mark_font' in asset_type:
                            mark_assets(ob)
                        if 'clear_font' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'CURVES':
                        if 'mark_curves' in asset_type:
                            mark_assets(ob)
                        if 'clear_curves' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'POINTCLOUD':
                        if 'mark_pointcloud' in asset_type:
                            mark_assets(ob)
                        if 'clear_pointcloud' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'VOLUME':
                        if 'mark_volume' in asset_type:
                            mark_assets(ob)
                        if 'clear_volume' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'GPENCIL':
                        if 'mark_greasepencil' in asset_type:
                            mark_assets(ob)
                        if 'clear_greasepencil' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'ARMATURE':
                        if 'mark_armature' in asset_type:
                            mark_assets(ob)
                        if 'clear_armature' in asset_type:
                            clear_assets(ob)
                    
                    if ob.type == 'LATTICE':
                        if 'mark_lattice' in asset_type:
                            mark_assets(ob)
                        if 'clear_lattice' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'EMPTY':
                        if 'mark_empty' in asset_type:
                            mark_assets(ob)
                        if 'clear_empty' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'LIGHT': 
                        if 'mark_light' in asset_type:
                            mark_assets(ob)
                        if 'clear_light' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'LIGHTPROBE':
                        if 'mark_lightprobe' in asset_type:
                            mark_assets(ob)
                        if 'clear_lightprobe' in asset_type:
                            clear_assets(ob)
                        
                    if ob.type == 'CAMERA':
                        if 'mark_camera' in asset_type:
                            mark_assets(ob)
                        if 'clear_camera' in asset_type:
                            clear_assets(ob)

                    if ob.type == 'SPEAKER':
                        if 'mark_speaker' in asset_type:
                            mark_assets(ob)
                        if 'clear_speaker' in asset_type:
                            clear_assets(ob)
                        

    if 'clear_object' in asset_type:
        for ob in bpy.data.objects:
            clear_assets(ob)
        for me in bpy.data.meshes:
            clear_assets(me)

            
    if 'materials_mark' in asset_type:
        for mat in bpy.data.materials:
            mark_assets(mat)    
    if 'materials_clear' in asset_type:
        for mat in bpy.data.materials:
            clear_assets(mat)

    if 'poses_mark' in asset_type:
        for pose in bpy.data.actions:
            mark_assets(pose)
    if 'poses_clear' in asset_type:
        for pose in bpy.data.actions:
            clear_assets(pose) 
     
    if 'worlds_mark' in asset_type:
        for world in bpy.data.worlds:
            mark_assets(world)
    if 'worlds_clear' in asset_type:
        for world in bpy.data.worlds:
            clear_assets(world)  
     

    #update all previews
    bpy.ops.wm.previews_ensure()

    #save the blend file to store asset marks
    bpy.ops.wm.save_mainfile()


def mark_assets(asset):
    asset.asset_mark()  
    if debug:
        print('    marking: ', asset.name)
        asset.asset_generate_preview()
    #bpy.ops.ed.lib_id_generate_preview()


def clear_assets(asset):
    if debug:
        print('    clearing: ', asset.name) 
    asset.asset_clear()
    asset.use_fake_user = True

paste_asset()
process_assets(argv=argv)

bpy.ops.wm.quit_blender()
'''
BLI_assert failed: C:\Repo\BlenderScripts\build_blender\BlenderGit\source\blender\windowmanager\intern\wm_window.c:2315, WM_opengl_context_create(), at 'BLI_thread_is_main()'

'''