import bpy

if bpy.context.active_object.mode != 'EDIT':
    
    bpy.ops.object.editmode_toggle()

bpy.ops.mesh.select_mode(type = 'VERT')
bpy.ops.mesh.select_non_manifold()

#bpy.ops.mesh.edge_face_add()
