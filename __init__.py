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
from bpy.types import AddonPreferences, Operator, Panel, PropertyGroup, UIList
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
        #blend_file = prefs().blend_file.replace(",", " ").split()   

        layout = self.layout   
        #layout.label(text="Mark Assets")
        for i in current_file:  
            layout.operator(operator="scene.asset_marker", text=i, icon='ASSET_MANAGER', emboss=True, depress=False).button_input=i
        layout.separator()

        """ layout.label(text="Mark in Blend Files")       

        for i in blend_file:  
            layout.operator(operator="scene.asset_marker", text=i, icon='FILE_BLEND', emboss=True, depress=False).button_input=i """



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
                
        if self.button_input == 'Mark_Objects':
            for ob in bpy.data.objects:
                ob.select_set(True)
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()
                    
        elif self.button_input == 'Mark_Meshes':
            for ob in bpy.data.meshes:
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()

        elif self.button_input == 'Mark_Materials':
            for ob in bpy.data.materials:
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()

        elif self.button_input == 'Mark_Textures':
            for ob in bpy.data.textures:
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()

        
   
class AssetWalker(Operator):
    bl_idname = "scene.asset_walker"
    bl_label = "asset_walker"
    bl_description = "mark library assets"
    
    button_input: StringProperty()
    blender_path = bpy.app.binary_path
    addon_path =  os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(addon_path, 'mark_assets.py')
    #blend_path = os.path.join(addon_path, 'assets.blend')
        

    def execute(self, context):        
            #print("button_input: ", self.button_input)
            self.asset_crawler(context)    

            return{'FINISHED'}

            
    def asset_crawler(self, context):
        print("crawl")  

        lib = prefs().asset_library
        lib_path =  bpy.context.preferences.filepaths.asset_libraries[lib].path
        
        ext = ('.blend')

        #print(lib_path)
        # iterating over directory and subdirectory to find all blender files and mark the desired assets
        for path, dirc, files in os.walk(lib_path):
            for name in files:
                if name.endswith(ext):
                    blend_path = os.path.join(path, name)
                    print(blend_path)  # printing file name
                    run([self.blender_path, 
                        blend_path, 
                        '--background', 
                        '--factory-startup', 
                        '--python', 
                        self.script_path, 
                        '--', str(prefs().objects), str(prefs().materials)
                    ], shell=True) 


        """ elif self.button_input == 'Mark_Objects_B':
            #blender myscene.blend --background --python myscript.py
            run([blender_path, blend_path, '--background', '--python', script_path, '--', self.button_input, str(state)], shell=True) 
        elif self.button_input == 'Mark_Meshes_B':
            #blender myscene.blend --background --python myscript.py
            run([blender_path, blend_path, '--background', '--python', script_path, '--', self.button_input, str(state)], shell=True) 
        elif self.button_input == 'Mark_Materials_B':
            #blender myscene.blend --background --python myscript.py
            run([blender_path, blend_path, '--background', '--python', script_path, '--', self.button_input, str(state)], shell=True) 
        elif self.button_input == 'Mark_Textures_B':
            #blender myscene.blend --background --python myscript.py
            run([blender_path, blend_path, '--background', '--python', script_path, '--', self.button_input, str(state)], shell=True)  """




lib = []    
def get_libs():   
    #lib = [v.name, v.name, v.name, 'ASSET_MANAGER', i for i,v in enumerate(bpy.context.preferences.filepaths.asset_libraries)] 
    #("all", "Blend File", 'Mark all Assets', 'FILE_BLEND', 0)
    for i,v in enumerate(bpy.context.preferences.filepaths.asset_libraries):
        #print((v.name, v.name, v.name, 'ASSET_MANAGER', i))
        lib.append((v.name, v.name, v.name, 'ASSET_MANAGER', i))
    print(lib)


class AssetMarkerPreferences(AddonPreferences):
    bl_idname = __package__
    
    current_file: StringProperty(
        name="current_file", 
        description="current_file", 
        subtype='NONE',
        default="Mark_Objects, Mark_Meshes, Mark_Materials, Mark_Textures",
        update=AM_PT_AssetMarker.draw)     

    type_options = [
        ("all", "Blend File", 'Mark all Assets', 'FILE_BLEND', 0),
        ("objects", "Objects", 'Mark Objects as Assets', 'MESH_PLANE', 1),
        ("meshes", "Meshes", 'Mark Meshes as Assets', 'MESH_CUBE', 2),
        ("materials", "Materials", 'Mark Materials as Assets', 'MESH_CIRCLE', 3),
        ("textures", "Textures", 'Mark Textures as Assets', 'MESH_UVSPHERE', 4),
    ]

    asset_type: EnumProperty(
        items=type_options,
        description="Select data type to mark as Asset",
        default="objects",
        #update=myfunction
    )    

    asset_library: EnumProperty(
        items=lib,
        description="asset_library",
        #default="all",
        update=get_libs()
    )

    asset_file: StringProperty(
        name="asset_file", 
        description="asset_file", 
        subtype='NONE',
        default="Default",
    )  

    objects: bpy.props.BoolProperty(
            name="objects",
            description="objects",
            default=True)      
    materials: bpy.props.BoolProperty(
            name="materials",
            description="materials",
            default=True)    

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
        layout.use_property_split = True 
        #layout.prop(self, 'current_file')
        layout.prop(self, 'asset_library')   
        layout.prop(self, 'objects', text='Objects')
        layout.prop(self, 'materials')
        layout.operator(operator="scene.asset_walker", text='Mark Library Assets', icon='FILE_BLEND', emboss=True, depress=False).button_input = 'walk_files'
        #template_list(listtype_name, list_id, dataptr, propname, active_dataptr, active_propname, item_dyntip_propname='', rows=5, maxrows=5, type='DEFAULT', columns=9, sort_reverse=False, sort_lock=False)
        


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
