import bpy
from collections import defaultdict
from mathutils import Vector

class HERITAGE_OT_VertexColor(bpy.types.Operator):

    bl_idname = "heritage.select_by_vertexcolor"
    bl_label = "Select by vertex color"
    bl_description = "Selects vertices based on color ID"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object and context.mode == 'EDIT_MESH'

    def execute(self, context):

        if bpy.context.active_object.mode == 'EDIT':
            
            bpy.ops.object.editmode_toggle()
        
        obj = bpy.context.active_object
        col = obj.data.vertex_colors.active
        polygons = obj.data.polygons

        color = getColor(obj)
        color = Vector(color)
        epsilon = 0.01

        vertex_map = defaultdict(list)

        for poly in polygons:
            for v_ix, l_ix in zip(poly.vertices, poly.loop_indices):
                vertex_map[v_ix].append(l_ix)
        
        for v_ix, l_ixs in vertex_map.items():
            for l_ix in l_ixs:
                
                comp = (color - Vector(col.data[l_ix].color)).length_squared

                if comp <= epsilon:
                    
                    obj.data.vertices[v_ix].select = True
                    
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_mode(type='FACE')    

        return {"FINISHED"}

def getColor(obj):

    obj = bpy.context.active_object

    colors = obj.data.vertex_colors.active.data
    selected_poly = list(filter(lambda p: p.select, obj.data.polygons))
        
    if len(selected_poly):

        p = selected_poly[0]
        r = g = b = 0
        
        for i in p.loop_indices:
            
            c = colors[i].color
            r += c[0]
            g += c[1]
            b += c[2]
            
        r /= p.loop_total
        g /= p.loop_total
        b /= p.loop_total
        
        color = (r, g, b, 1.0)

        return color

    else:

        return (0, 0, 0, 1.0)