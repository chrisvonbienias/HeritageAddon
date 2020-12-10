import bpy
from collections import defaultdict
from mathutils import Vector

class VIEW3D_OT_vertexColor(bpy.types.Operator):

    bl_idname = "view3d.select_by_vertexcolor"
    bl_label = "Select by vertex color"
    bl_description = "Selects vertices based on color ID"

    def execute(self, context):

        obj = bpy.context.active_object
        col = obj.data.vertex_colors.active
        polygons = obj.data.polygons

        color = Vector((1, 1, 0, 0))
        epsilon = 0.01

        vertex_map = defaultdict(list)

        for poly in polygons:
            for v_ix, l_ix in zip(poly.vertices, poly.loop_indices):
                vertex_map[v_ix].append(l_ix)
        
        for v_ix, l_ixs in vertex_map.items():
            for l_ix in l_ixs:
                
                comp = (color - Vector(col.data[l_ix].color)).length_squared

                if comp < 1.0 + epsilon:
                    
                    obj.data.vertices[v_ix].select = True
                    
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_mode(type='FACE')    

        return {"FINISHED"}