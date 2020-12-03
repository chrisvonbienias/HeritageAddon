import bpy
import random
import math
import bmesh

class VIEW3D_OT_vertexColor(bpy.types.Operator):

    bl_idname = "view3d.select_by_vertexcolor"
    bl_label = "Select by vertex color"
    bl_description = "Selects vertices based on color ID"

    def execute(self, context):
        
        bpy.ops.object.editmode_toggle()
        so = bpy.context.active_object
        bm = bmesh.from_edit_mesh(so.data)

        vertices = [e for e in bm.verts]

        for vert in vertices:
            
            rand = round(random.random())
            
            if rand :

                vert.select = True

            else:

                vert.select = False

        bmesh.update_edit_mesh(so.data, True)
        bm.free()

        return {"FINISHED"}