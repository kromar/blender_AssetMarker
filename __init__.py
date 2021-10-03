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
from bpy.props import BoolProperty, StringProperty, EnumProperty


bl_info = {
    "name": "Asset Marker",
    "description": "Mark Assets in blend files",
    "author": "Daniel Grauer",
    "version": (1, 1, 0),
    "blender": (3, 0, 0),
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
    
    def set_mark(self, ob, state=False):   
        if state:
            ob.asset_mark()
            try:
                bpy.ops.file.select()
                bpy.ops.ed.lib_id_generate_preview()
            except:
                pass                                    
        else:
            ob.asset_clear()  


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
                        
   
class AssetWalker(Operator):
    bl_idname = "scene.asset_walker"
    bl_label = "asset_walker"
    bl_description = "mark library assets"
    
    button_input: StringProperty()
    blender_path = bpy.app.binary_path
    addon_path =  os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(addon_path, 'mark_assets.py')        


    def execute(self, context):        
        self.asset_crawler(context)    
        return{'FINISHED'}

            
    def asset_crawler(self, context):
        # iterating over directory and subdirectory to find all blender files and mark the desired assets
        lib = prefs().asset_library
        lib_path =  bpy.context.preferences.filepaths.asset_libraries[lib].path
        for path, dirc, files in os.walk(lib_path):
            for name in files:
                if name.endswith('.blend'):
                    blend_path = os.path.join(path, name)
                    #print(blend_path)  # printing file name
                    run([self.blender_path, 
                        blend_path, 
                        '--background', 
                        '--factory-startup',
                        '--python', 
                        self.script_path, 
                        '--', 
                        str(prefs().objects), 
                        str(prefs().materials),
                        str(prefs().meshes),
                        str(prefs().textures),
                    ], shell=True) 


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
        description="Select Asset Library to Mark. Shows configured Asset Libraries",
        #default="all",
        update=get_libs()
    )

    objects: bpy.props.BoolProperty(
            name="objects",
            description="objects",
            default=True)      
    materials: bpy.props.BoolProperty(
            name="materials",
            description="materials",
            default=True)    
    meshes: bpy.props.BoolProperty(
            name="meshes",
            description="meshes",
            default=False)      
    textures: bpy.props.BoolProperty(
            name="textures",
            description="textures",
            default=False)   

    '''
    asset_data = [
        'actions',
        'armatures',
        'brushes',
        'cameras',
        'collections',
        'curves',
        'fonts',
        'grease_pencils',
        'hairs',
        'images',
        'lattices',
        'libraries',
        'lightprobes',
        'lights',
        'linestyles',
        'masks',
        'materials',
        'meshes',
        'metaballs',
        'movieclips',
        'node_groups',
        'objects',
        'paint_curves',
        'palettes',
        'particles',
        'pointclouds',
        'scenes',
        'screens',
        'shape_keys',
        'simulations',
        'sounds',
        'speakers',
        'texts',
        'textures',
        'version',
        'volumes',
        'workspaces',
        'worlds',
    ]
    #'''
     
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        
        box = layout.box() 
        row = box.row()
        row.prop(self, 'asset_library', text="Mark Assets in")
        box.operator(operator="scene.asset_walker", text='Mark Library Assets', icon='FILE_BLEND', emboss=True, depress=False).button_input = 'walk_files'
        
        box.prop(self, 'objects', text='Objects')
        box.prop(self, 'materials')
        box.prop(self, 'meshes')
        box.prop(self, 'textures')
        #template_list(listtype_name, list_id, dataptr, propname, active_dataptr, active_propname, item_dyntip_propname='', rows=5, maxrows=5, type='DEFAULT', columns=9, sort_reverse=False, sort_lock=False)

        #asset libraries
        paths = context.preferences.filepaths

        box = layout.box()
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
