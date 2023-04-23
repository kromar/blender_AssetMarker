import bpy

def process_assets(mode):    
    if mode: 
        print('marking objects:')
        for ob in bpy.data.objects:
            for i in bpy.data.scenes:  #only mark objects that are linked to a scene
                if ob.name in bpy.data.scenes[i.name].objects and ob.type == 'MESH':
                    mark_assets(ob)
    else:
        print('clearing objects:')
        for ob in bpy.data.objects:
            clear_assets(ob)
        for me in bpy.data.meshes:
            clear_assets(me)            

    if mode:  
        print('marking materials')
        for mat in bpy.data.materials:
            mark_assets(mat)
    else:
        print('clearing materials')
        for mat in bpy.data.materials:
            clear_assets(mat) 
            
    #bpy.ops.wm.previews_batch_generate()
    bpy.ops.wm.previews_ensure()           

def mark_assets(asset):
    print('    ', asset.name)
    asset.asset_mark()  
    asset.asset_generate_preview()
    bpy.ops.ed.lib_id_generate_preview()

def clear_assets(asset):
    print('    ', asset.name) 
    asset.asset_clear()
    asset.use_fake_user = True
    
process_assets(True)