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
from bpy.props import BoolProperty, StringProperty, IntProperty


bl_info = {
    "name": "Asset Manager",
    "description": "Manage your Assets in .blend files",
    "author": "Daniel Grauer",
    "version": (1, 3, 0),
    "blender": (3, 0, 0),
    "location": "Sidebar",
    "category": "System",
    "wiki_url": "https://github.com/kromar/blender_AssetManager",
    "tracker_url": "https://github.com/kromar/blender_AssetManager/issues",
}


def prefs():
    ''' load addon preferences to reference in code'''
    user_preferences = bpy.context.preferences
    return user_preferences.addons[__package__].preferences 


class AM_PT_AssetManager(Panel):    
    bl_label = 'Asset Manager'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Asset Manager'      

    def draw(self, context):       
        current_file = prefs().current_file.replace(",", " ").split()
        layout = self.layout   
        for i in current_file:  
            layout.operator(operator="scene.asset_manager", text=i, icon='ASSET_MANAGER', emboss=True, depress=False).button_input=i
        layout.separator()


class AssetManager(Operator):
    bl_idname = "scene.asset_manager"
    bl_label = "asset_manager"
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
        if self.button_input == 'Mark_Collections':                                  
            for ob in bpy.data.collections:
                if state:
                    self.mark_assets(ob) 
                else:
                    self.clear_assets(ob)      

        elif self.button_input == 'Mark_Objects':                                  
            for ob in bpy.data.objects:
                if state:
                    self.mark_assets(ob) 
                else:
                    self.clear_assets(ob)    

        elif self.button_input == 'Mark_Materials':
            for ob in bpy.data.materials:
                if state:
                    self.mark_assets(ob) 
                else:
                    self.clear_assets(ob)

        elif self.button_input == 'Mark_Poses':
            for ob in bpy.data.actions:
                if state:
                    self.mark_assets(ob) 
                else:
                    self.clear_assets(ob)

        elif self.button_input == 'Mark_Worlds':
            for ob in bpy.data.worlds:
                if state:
                    self.mark_assets(ob) 
                else:
                    self.clear_assets(ob)

        elif self.button_input == 'Mark_NodeGroups':
            for ob in bpy.data.node_groups:
                if state:
                    self.mark_assets(ob) 
                else:
                    self.clear_assets(ob)

                           
    def mark_assets(self, asset):
        if prefs().debug_mode:
            print('    Mark as Asset 1: ', asset.name)
        asset.asset_mark()  
        asset.asset_generate_preview()

    def clear_assets(self, asset):
        if prefs().debug_mode:
            print('    Clear Asset 1: ', asset.name) 
        asset.asset_clear()
        asset.use_fake_user = True        
                        
   
class AssetWalker(Operator):
    bl_idname = "scene.asset_walker"
    bl_label = "Mark Assets"
    bl_description = "mark library assets"
    
    blender_path: str = bpy.app.binary_path
    addon_path: str = os.path.abspath(os.path.dirname(__file__))
    script_path: str = os.path.join(addon_path, 'mark_assets.py')  
    
    button_input: StringProperty()      
    library_index: IntProperty()

    def execute(self, context): 
        print("\nRun Asset Crawler")
        self.asset_crawler(context)  
        
        return{'FINISHED'}

    def convert_args_to_cmdlist(self):
        arg_list = []
        if prefs().mark_objects:
            arg_list.append('mark_objects')

            if prefs().mark_mesh:
                arg_list.append('mark_mesh')
            else:            
                arg_list.append('clear_mesh')

            if prefs().mark_surface:
                arg_list.append('mark_surface')
            else:            
                arg_list.append('clear_surface')

            if prefs().mark_meta:
                arg_list.append('mark_meta')
            else:            
                arg_list.append('clear_meta')

            if prefs().mark_curve:
                arg_list.append('mark_curve')
            else:            
                arg_list.append('clear_curve')

            if prefs().mark_font:
                arg_list.append('mark_font')
            else:            
                arg_list.append('clear_font')

            if prefs().mark_curves:
                arg_list.append('mark_curves')
            else:            
                arg_list.append('clear_curves')

            if prefs().mark_pointcloud:
                arg_list.append('mark_pointcloud')
            else:            
                arg_list.append('clear_pointcloud')

            if prefs().mark_volume:
                arg_list.append('mark_volume')
            else:            
                arg_list.append('clear_volume')

            if prefs().mark_greasepencil:
                arg_list.append('mark_greasepencil')
            else:            
                arg_list.append('clear_greasepencil')

            if prefs().mark_armature:
                arg_list.append('mark_armature')
            else:            
                arg_list.append('clear_armature')

            if prefs().mark_lattice:
                arg_list.append('mark_lattice')
            else:            
                arg_list.append('clear_lattice')

            if prefs().mark_empty:
                arg_list.append('mark_empty')
            else:            
                arg_list.append('clear_empty')

            if prefs().mark_light:
                arg_list.append('mark_light')
            else:            
                arg_list.append('clear_light')

            if prefs().mark_lightprobe:
                arg_list.append('mark_lightprobe')
            else:            
                arg_list.append('clear_lightprobe')

            if prefs().mark_camera:
                arg_list.append('mark_camera')
            else:            
                arg_list.append('clear_camera')

            if prefs().mark_speaker:
                arg_list.append('mark_speaker')
            else:            
                arg_list.append('clear_speaker')

        else:            
            arg_list.append('clear_object')


        if prefs().mark_collections:
            arg_list.append('mark_collections')
        else:            
            arg_list.append('clear_collections')

        if prefs().mark_materials:
            arg_list.append('mark_materials')
        else:            
            arg_list.append('clear_materials')

        if prefs().mark_poses:
            arg_list.append('mark_poses')
        else:            
            arg_list.append('clear_poses')

        if prefs().mark_worlds:
            arg_list.append('mark_worlds')
        else:            
            arg_list.append('clear_worlds')
            
        if prefs().mark_nodegroups:
            arg_list.append('mark_nodegroups')
        else:            
            arg_list.append('clear_nodegroups')

        asset_type = ' '.join([str(item) for item in arg_list])
        return asset_type


    def asset_crawler(self, context):
        # iterating over directory and subdirectory to find all blender files 
        # and mark the desired assets
        asset_type = self.convert_args_to_cmdlist()

        paths = context.preferences.filepaths
        lib_path = paths.asset_libraries[self.library_index].path

        # Count total files first
        total_files = 0
        for path, dirc, files in os.walk(lib_path):
            total_files += len([f for f in files if f.endswith('.blend')])
        
        wm = bpy.context.window_manager
        wm.progress_begin(0, total_files)
        current_file = 0

        for path, dirc, files in os.walk(lib_path):          
            for name in files:
                if name.endswith('.blend'):                   
                    blend_path = os.path.join(path, name)
                    print("Opening Asset Library: ", blend_path)

                    run([self.blender_path, 
                        blend_path, 
                        '--background', 
                        '--factory-startup',
                        '--python', 
                        self.script_path, 
                        '--', 
                        str(prefs().debug_mode), #arg 0
                        asset_type,  #arg 1
                    ], shell=True)
                    
                    # Update progress after processing each file
                    current_file += 1
                    wm.progress_update(current_file)
                    
                    for window in bpy.context.window_manager.windows:
                        screen = window.screen
                        for area in screen.areas:
                            if area.type == 'FILE_BROWSER':  
                                pass
        
        wm.progress_end()
        return{'FINISHED'}


class AssetManagerPreferences(AddonPreferences):
    bl_idname = __package__
    
    current_file: StringProperty(
        name="current_file", 
        description="current_file", 
        subtype='NONE',
        default="Mark_Collections, Mark_Objects, Mark_Materials, Mark_Poses, Mark_Worlds, Mark_NodeGroups",
        update=AM_PT_AssetManager.draw)

    mark_collections: BoolProperty(
            name="Collections",
            description="All Collections will be marked as Assets",
            default=False)  
    
    mark_objects: BoolProperty(
            name="Objects",
            description="All Objects will be marked as Assets",
            default=True)   
            
    custom_object_types: BoolProperty(
            name="Configure Object Types",
            description="debug_mode",
            default=False)  

    mark_mesh: BoolProperty(
            name="Mesh",
            description="All Meshes will be marked as Assets",
            default=True)  
    
    mark_surface: BoolProperty(
            name="Surface",
            description="All Surfaces will be marked as Assets",
            default=True) 
    
    mark_meta: BoolProperty(
            name="Meta",
            description="All Metas will be marked as Assets",
            default=True) 

    mark_curve: BoolProperty(
            name="Curve",
            description="All Curves will be marked as Assets",
            default=True) 
    
    mark_font: BoolProperty(
            name="Font",
            description="All Fonts will be marked as Assets",
            default=True) 
    
    mark_curves: BoolProperty(
            name="Curves",
            description="All Curves will be marked as Assets",
            default=True) 
    
    mark_pointcloud: BoolProperty(
            name="Pointcloud",
            description="All Pointclouds will be marked as Assets",
            default=True) 
    
    mark_volume: BoolProperty(
            name="Volume",
            description="All Volumes will be marked as Assets",
            default=True) 
    
    mark_greasepencil: BoolProperty(
            name="Grease Pencil",
            description="All Grease Pencils will be marked as Assets",
            default=True) 
    
    mark_armature: BoolProperty(
            name="Armatures",
            description="All Armatures will be marked as Assets",
            default=True) 
    
    mark_lattice: BoolProperty(
            name="Lattice",
            description="All Lattices will be marked as Assets",
            default=True) 
    
    mark_empty: BoolProperty(
            name="Empties",
            description="All Empties will be marked as Assets",
            default=True) 
    
    mark_light: BoolProperty(
            name="Light",
            description="All Lights will be marked as Assets",
            default=True) 
    
    mark_lightprobe: BoolProperty(
            name="Lightprobe",
            description="All Lightprobes will be marked as Assets",
            default=True) 
    
    mark_camera: BoolProperty(
            name="Camera",
            description="All Cameras will be marked as Assets",
            default=True) 
    
    mark_speaker: BoolProperty(
            name="Speaker",
            description="All Speakers will be marked as Assets",
            default=True) 
               

    mark_materials: BoolProperty(
            name="Materials",
            description="All Materials will be marked as Assets",
            default=True)   
                     
    mark_poses: BoolProperty(
            name="Poses",
            description="All Poses will be marked as Assets",
            default=False) 
      
    mark_worlds: BoolProperty(
            name="Worlds",
            description="All Worlds will be marked as Assets",
            default=False)  
    
    mark_nodegroups: BoolProperty(
            name="Node Groups",
            description="All Node Groups will be marked as Assets",
            default=False)  
 
    debug_mode: BoolProperty(
            name="debug_mode",
            description="debug_mode",
            default=True)  
            
     
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False            
        layout.prop(self, 'debug_mode')    
        
        #asset libraries
        paths = context.preferences.filepaths
        box = layout.box()
        row = box.row()
        box.label(text='Asset Libraries')
        split = box.split(factor=0.3)
        name_col = split.column()
        path_col = split.column()
        asset_col = split.column()

        row = name_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Name")

        row = path_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Path")

        row = asset_col.row(align=True)  # Padding
        row.separator()
        row.label(text="Asset Manager")

        for i, library in enumerate(paths.asset_libraries):
            name_col.prop(library, "name", text="")
            row = path_col.row()
            row.prop(library, "path", text="") 
            row = asset_col.row()           
            row.operator(operator="scene.asset_walker", icon='ASSET_MANAGER', emboss=True, depress=False).library_index = i
            row.operator("preferences.asset_library_remove", text="", icon='TRASH', emboss=True).index = i
         
        row = box.row()
        row.alignment = 'LEFT'
        row.operator("preferences.asset_library_add", text="", icon='ADD', emboss=False)
        

        # Asset Manager selection
        box = layout.box() 
        box.label(text='Asset Manager Configuration')       
        col = box.column()
        split = col.split()   
        col1 = split.column()  
        col2 = split.column()  
        col3 = split.column()  

        col1.prop(self, 'mark_collections',icon = 'OUTLINER_COLLECTION')
        col1.prop(self, 'mark_objects',icon = 'OBJECT_DATA')
        if self.mark_objects:
            col1.prop(self, 'custom_object_types')            
            col1 = col1.column(align=True) 
            if self.custom_object_types:
                col1.prop(self, 'mark_mesh',icon = 'OUTLINER_OB_MESH')
                col1.prop(self, 'mark_surface',icon = 'OUTLINER_OB_SURFACE')
                col1.prop(self, 'mark_meta',icon = 'OUTLINER_OB_META')
                col1.prop(self, 'mark_curve',icon = 'OUTLINER_OB_CURVE')
                col1.prop(self, 'mark_font',icon = 'OUTLINER_OB_FONT')
                if bpy.app.version >= (3,2,0):
                    col1.prop(self, 'mark_curves',icon = 'OUTLINER_OB_CURVES')
                col1.prop(self, 'mark_pointcloud',icon = 'OUTLINER_OB_POINTCLOUD')
                col1.prop(self, 'mark_volume',icon = 'OUTLINER_OB_VOLUME')
                col1.prop(self, 'mark_greasepencil',icon = 'OUTLINER_OB_GREASEPENCIL')
                col1.prop(self, 'mark_armature',icon = 'OUTLINER_OB_ARMATURE')
                col1.prop(self, 'mark_lattice',icon = 'OUTLINER_OB_LATTICE')
                col1.prop(self, 'mark_empty',icon = 'OUTLINER_OB_EMPTY')
                col1.prop(self, 'mark_light',icon = 'OUTLINER_OB_LIGHT')
                col1.prop(self, 'mark_lightprobe',icon = 'OUTLINER_OB_LIGHTPROBE')
                col1.prop(self, 'mark_camera',icon = 'OUTLINER_OB_CAMERA')
                col1.prop(self, 'mark_speaker',icon = 'OUTLINER_OB_SPEAKER')
               
        col2.prop(self, 'mark_materials', icon = 'MATERIAL')
        col2.prop(self, 'mark_worlds', icon = 'WORLD')
        col3.prop(self, 'mark_poses', icon = 'POSE_HLT')
        col3.prop(self, 'mark_nodegroups', icon = 'NODETREE')

        #template_list(listtype_name, list_id, dataptr, propname, active_dataptr, active_propname, item_dyntip_propname='', rows=5, maxrows=5, type='DEFAULT', columns=9, sort_reverse=False, sort_lock=False)




class ASSETBROWSER_MT_asset_manager_menu(bpy.types.Menu):
    bl_label = "Asset Manager"
    bl_idname = "ASSETBROWSER_MT_asset_manager_menu"

    def draw(self, _context):
        layout = self.layout
        layout.operator("scene.asset_remove", icon='TRASH')
        #layout.operator("scene.asset_manager", text="Mark Assets")
        #layout.operator("scene.asset_walker", text="Crawl Library")


class RemoveAsset(Operator):
    bl_idname = "scene.asset_remove"
    bl_label = "Remove Selected Assets"
    bl_description = "Remove asset mark from selected assets"
    
    def execute(self, _context):
        # Count total assets first
        selected_assets = list(bpy.context.selected_assets)
        total_assets = len(selected_assets)
        
        if total_assets == 0:
            return {'FINISHED'}
        
        wm = bpy.context.window_manager
        wm.progress_begin(0, total_assets)
        current_asset = 0
        
        # for selected asset, open the source blend file, clear the asset mark and save the blend file
        for asset in selected_assets:
            print("Asset: ", asset.name)
            print("  Asset path: ", asset.full_library_path)
            print("  Asset type: ", asset.id_type)
            
            # open the blend file, clear the asset mark and save the blend file
            blend_path = asset.full_library_path
            run([bpy.app.binary_path, 
                blend_path, 
                '--background', 
                '--factory-startup',
                '--python', 
                os.path.join(os.path.abspath(os.path.dirname(__file__)), 'remove_asset.py'), 
                '--', 
                str(prefs().debug_mode),      #arg 0
                str(asset.id_type),           #arg 1
                str(asset.name),              #arg 2
            ], shell=True)
            
            # Update progress after processing each asset
            current_asset += 1
            wm.progress_update(current_asset)

        wm.progress_end()
        
        # Refresh asset library to update previews
        bpy.ops.asset.library_refresh()
        
        return {'FINISHED'}


def assetbrowser_menu_draw(self, _context):
    self.layout.menu("ASSETBROWSER_MT_asset_manager_menu")

bpy.types.ASSETBROWSER_MT_editor_menus.append(assetbrowser_menu_draw)
    


classes = (
    RemoveAsset,
    AssetManager,
    AssetWalker,
    AM_PT_AssetManager,
    AssetManagerPreferences,
    ASSETBROWSER_MT_asset_manager_menu,
    )


def register():    
    [bpy.utils.register_class(c) for c in classes]


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]


if __name__ == "__main__":
    register()
