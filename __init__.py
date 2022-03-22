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
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import os   
from subprocess import run
from bpy.types import AddonPreferences, Operator, Panel
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty


bl_info = {
    "name": "Asset Marker",
    "description": "Mark Assets in .blend files",
    "author": "Daniel Grauer",
    "version": (1, 2, 2),
    "blender": (3, 1, 0),
    "location": "Sidebar",
    "category": "System",
    "wiki_url": "https://github.com/kromar/blender_AssetMarker",
    "tracker_url": "https://github.com/kromar/blender_AssetMarker/issues",
}


def prefs():
    ''' load addon preferences to reference in code'''
    user_preferences = bpy.context.preferences
    return user_preferences.addons[__package__].preferences 


class AM_PT_AssetMarker(Panel):    
    bl_label = 'Asset Marker'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Asset Marker'      

    def draw(self, context):       
        current_file = prefs().current_file.replace(",", " ").split()
        layout = self.layout   
        for i in current_file:  
            layout.operator(operator="scene.asset_marker", text=i, icon='ASSET_MANAGER', emboss=True, depress=False).button_input=i
        layout.separator()


class AssetMarker(Operator):
    bl_idname = "scene.asset_marker"
    bl_label = "asset_marker"
    bl_description = "mark assets"
    
    button_input: StringProperty()
        
    asset_marked: BoolProperty(
        name="asset_marked",
        description="asset_marked",
        default=False)
        
    mesh_type: BoolProperty(
        name="mesh_type",
        description="mesh_type",
        default=False)


    def execute(self, context):        
        #print("button_input: ", self.button_input)
        if self.asset_marked:
            self.asset_marked = False
        else:
            self.asset_marked = True  
        self.mark_asset(self.asset_marked)   

        return{'FINISHED'}
    

    def mark_asset(self, state = False):          
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'FILE_BROWSER':  
                    if self.button_input == 'Mark_Objects':                                  
                        for ob in bpy.data.objects:
                            ob.select_set(True)
                            self.set_mark(ob, state)                                                               
                            #ob.select_set(False)                                    
                    elif self.button_input == 'Mark_Meshes':
                        for ob in bpy.data.meshes:
                            self.set_mark(ob, state)    
                    elif self.button_input == 'Mark_Materials':
                        for ob in bpy.data.materials:
                            self.set_mark(ob, state)  
                    elif self.button_input == 'Mark_Textures':
                        for ob in bpy.data.textures:
                            self.set_mark(ob, state)  
                           
                                
    def set_mark(self, ob, state=False):
        print("set mark: ", ob.name)   
        if state:
            ob.asset_mark()
            try:
                bpy.ops.file.select()
                #bpy.ops.ed.lib_id_generate_preview()
            except:
                pass                                    
        else:
            ob.asset_clear()  
                        
   
class AssetWalker(Operator):
    bl_idname = "scene.asset_walker"
    bl_label = "Mark Assets"
    bl_description = "mark library assets"
    
    blender_path = bpy.app.binary_path
    addon_path =  os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(addon_path, 'mark_assets.py')  
    
    button_input: StringProperty()      
    index: IntProperty()

    def execute(self, context): 
        print("\nRun Asset Crawler")  

        self.asset_crawler(context)  
        return{'FINISHED'}

            
    def asset_crawler(self, context):
        # iterating over directory and subdirectory to find all blender files 
        # and mark the desired assets

        arg_list = []
        if prefs().mark_objects:
            arg_list.append('object_mark')
        else:            
            arg_list.append('object_clear')

        if prefs().mark_materials:
            arg_list.append('materials_mark')
        else:            
            arg_list.append('materials_clear')

        if prefs().mark_poses:
            arg_list.append('poses_mark')
        else:            
            arg_list.append('poses_clear')

        if prefs().mark_worlds:
            arg_list.append('worlds_mark')
        else:            
            arg_list.append('worlds_clear')

        print(arg_list)
        asset_type = ' '.join([str(item) for item in arg_list])
        print(asset_type)

        #lib = prefs().asset_library
        #lib_path =  bpy.context.preferences.filepaths.asset_libraries[lib].path
        
        paths = context.preferences.filepaths
        print("ASSET LIB: ", paths.asset_libraries[self.index].name)
        lib_path = paths.asset_libraries[self.index].path

        for path, dirc, files in os.walk(lib_path):          
            for name in files:
                if name.endswith('.blend'):
                    try:
                        blend_path = os.path.join(path, name)
                        print("Opening Asset Library: ", blend_path)     #0
                        #""" 
                        run([self.blender_path, 
                            blend_path, 
                            '--background', 
                            '--factory-startup',
                            '--python', 
                            self.script_path, 
                            '--', 
                            str(prefs().debug_mode),    #0
                            asset_type,                 #1
                        ], shell=False)  
                        #""" 
                    except:
                        print("cant open %, file corrupt?", name)  
                
            #print("amount of files", len(files))  

            """ 
            progress_total = len(files)
            wm = bpy.context.window_manager
            wm.progress_begin(0, progress_total)       
            for i in range(progress_total):
                wm.progress_update(i)   
                print(i)
            wm.progress_end() 
            #"""

        return{'FINISHED'}


libraries = []    
def get_libs():  
    libraries.clear()
    #("all", "Blend File", 'Mark all Assets', 'FILE_BLEND', 0)
    for i,v in enumerate(bpy.context.preferences.filepaths.asset_libraries):
        libraries.append((v.name, v.name, v.name, 'ASSET_MANAGER', i))


class AssetMarkerPreferences(AddonPreferences):
    bl_idname = __package__
    
    current_file: StringProperty(
        name="current_file", 
        description="current_file", 
        subtype='NONE',
        default="Mark_Objects, Mark_Meshes, Mark_Materials, Mark_Textures",
        update=AM_PT_AssetMarker.draw)     

    asset_library: EnumProperty(
        items=libraries,
        name='',
        description="Select Asset Library to Mark",
        #default="all",
        update=get_libs())

    mark_objects: bpy.props.BoolProperty(
            name="Objects",
            description="All Objects will be marked as Assets",
            default=True)   
            
    """
    'MESH', 'CURVE', 'SURFACE', 'META', 'FONT',     
    'CURVES', 'POINTCLOUD', 'VOLUME', 'GPENCIL', 
    'ARMATURE', 'LATTICE', 'EMPTY', 
    'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER
    """

    mark_materials: bpy.props.BoolProperty(
            name="Materials",
            description="All Materials will be marked as Assets",
            default=True)                    
    mark_poses: bpy.props.BoolProperty(
            name="Poses",
            description="All Poses will be marked as Assets",
            default=False)   
    mark_worlds: bpy.props.BoolProperty(
            name="Worlds",
            description="All Worlds will be marked as Assets",
            default=False)  
 
    debug_mode: bpy.props.BoolProperty(
            name="debug_mode",
            description="debug_mode",
            default=False)  
     
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False    
        
        layout.prop(self, 'debug_mode')    
        box = layout.box() 
        row = box.row()
        #row.prop(self, 'asset_library')
        #row.operator(operator="scene.asset_walker", icon='FILE_BLEND', emboss=True, depress=False).button_input = 'walk_files'
           
        col = box.column()
        split = col.split(factor = 0.3)   
        col1 = split.column()  
        col2 = split.column()  
        col3 = split.column()  
        col1.prop(self, 'mark_objects',icon = 'OBJECT_DATA')
        col2.prop(self, 'mark_materials', icon = 'MATERIAL')
        #col2.prop(self, 'mark_textures', icon = 'TEXTURE')
        col2.prop(self, 'mark_worlds', icon = 'WORLD')
        col3.prop(self, 'mark_poses', icon = 'POSE_HLT')

        #template_list(listtype_name, list_id, dataptr, propname, active_dataptr, active_propname, item_dyntip_propname='', rows=5, maxrows=5, type='DEFAULT', columns=9, sort_reverse=False, sort_lock=False)

        row = box.row()
        #asset libraries
        paths = context.preferences.filepaths

        box = layout.box()
        box.label(text='Asset Libraries')
        split = box.split(factor=0.35)
        name_col = split.column()
        path_col = split.column()

        row = name_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Name")

        row = path_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Path")

        for i, library in enumerate(paths.asset_libraries):
            name_col.prop(library, "name", text="")
            row = path_col.row()
            row.prop(library, "path", text="")
            row.operator("preferences.asset_library_remove", text="", icon='X', emboss=False).index = i
            row.operator(operator="scene.asset_walker", icon='FILE_BLEND', emboss=True, depress=False).index = i
         
        row = box.row()
        row.alignment = 'LEFT'
        row.operator("preferences.asset_library_add", text="", icon='ADD', emboss=False)



classes = (
    AssetMarker,
    AssetWalker,
    AM_PT_AssetMarker,
    AssetMarkerPreferences,
    )


def register():    
    [bpy.utils.register_class(c) for c in classes]


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]


if __name__ == "__main__":
    register()
