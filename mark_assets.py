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
#   1:asset_type
# ]

argv = argv[argv.index("--") + 1:]  # get all args after "--"
debug = True

if argv[0] == 'True':
    debug = True
    print(argv)
else:
    debug = False


def process_assets(argv):
    bpy.ops.wm.previews_clear()
    
    # 1. store render engine and switch to EEVEE for preview creation
    render_engine = bpy.context.scene.render.engine    
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    # 2. Lower the samples so the "complex shader" doesn't choke
    # This ensures each thumbnail takes milliseconds, not minutes
    render_samples = bpy.context.scene.eevee.taa_render_samples 
    bpy.context.scene.eevee.taa_render_samples = 1

    #bpy.ops.wm.previews_batch_clear()
    asset_type = argv[1].split()
    if not debug:
        print("asset_type: ", asset_type)    
    if 'mark_objects' in asset_type:
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

            
    if 'mark_materials' in asset_type:
        for mat in bpy.data.materials:
            mark_assets(mat)    
    if 'clear_materials' in asset_type:
        for mat in bpy.data.materials:
            clear_assets(mat)

    if 'mark_poses' in asset_type:
        for pose in bpy.data.actions:
            mark_assets(pose)
    if 'clear_poses' in asset_type:
        for pose in bpy.data.actions:
            clear_assets(pose) 
     
    if 'mark_worlds' in asset_type:
        for world in bpy.data.worlds:
            mark_assets(world)
    if 'clear_worlds' in asset_type:
        for world in bpy.data.worlds:
            clear_assets(world)              
     
    if 'mark_collections' in asset_type:
        for collection in bpy.data.collections:
            mark_assets(collection)
    if 'clear_collections' in asset_type:
        for collection in bpy.data.collections:
            clear_assets(collection)  
     
    if 'mark_nodegroups' in asset_type:
        for group in bpy.data.node_groups:
            mark_assets(group)
    if 'clear_nodegroups' in asset_type:
        for group in bpy.data.node_groups:
            clear_assets(group)   
    
    #restore render engine
    bpy.context.scene.eevee.taa_render_samples = render_samples
    bpy.context.scene.render.engine = render_engine

    #save the blend file to store asset marks
    print('save_mainfile')
    bpy.ops.wm.save_mainfile()


def mark_assets(asset):
    if debug:
        print('    Mark as Asset: ', asset.name)
    asset.asset_mark()  
    asset.asset_generate_preview()


def clear_assets(asset):
    if debug:
        print('    Clear Asset: ', asset.name) 
    asset.asset_clear()
    asset.use_fake_user = True


process_assets(argv=argv)


'''
BLI_assert failed: C:\Repo\BlenderScripts\build_blender\BlenderGit\source\blender\windowmanager\intern\wm_window.c:2315, WM_opengl_context_create(), at 'BLI_thread_is_main()'

'''