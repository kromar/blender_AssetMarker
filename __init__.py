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
from bpy.types import AddonPreferences, Operator, Panel
from bpy.props import BoolProperty, StringProperty, EnumProperty


bl_info = {
    "name": "Asset Marker",
    "description": "Mark Assets in blend files",
    "author": "Daniel Grauer",
    "version": (1, 0, 0),
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

class CM_PT_AssetMarker(Panel):    
    bl_label = 'Asset Marker'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AssetMarker'

    def draw(self, context):       
        prefix = prefs().collection_prefix.replace(",", " ").split()        
        layout = self.layout    
        for i in prefix:  
            layout.operator(operator="scene.asset_marker", text=i, icon='ASSET_MANAGER', emboss=True, depress=False).button_input=i


class AssetMarker_OT_run(Operator):
    bl_idname = "scene.asset_marker"
    bl_label = "asset_marker"
    bl_description = "mark assets"
    
    button_input: StringProperty()
        
    asset_marked: BoolProperty(
        name="asset_marked",
        description="asset_marked",
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

        if self.button_input == 'Objects':
            for ob in bpy.data.objects:
                ob.select_set(True)
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()
                    
        elif self.button_input == 'Meshes':
            for ob in bpy.data.meshes:
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()

        elif self.button_input == 'Materials':
            for ob in bpy.data.materials:
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()

        elif self.button_input == 'Textures':
            for ob in bpy.data.textures:
                if state:
                    ob.asset_mark()
                else:
                    ob.asset_clear()

       

class AssetMarkerPreferences(AddonPreferences):
    bl_idname = __package__

    collection_prefix: StringProperty(
        name="collection_prefix", 
        description="collection_prefix", 
        subtype='NONE',
        default="Objects, Meshes, Materials, Textures",
        update=CM_PT_AssetMarker.draw)     

    mesh_type: BoolProperty(
        name="mesh_type",
        description="mesh_type",
        default=False)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True 
        layout.prop(self, 'collection_prefix')
        


classes = (
    AssetMarker_OT_run,
    CM_PT_AssetMarker,
    AssetMarkerPreferences,
    )

def register():    
    [bpy.utils.register_class(c) for c in classes]


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
    register()
