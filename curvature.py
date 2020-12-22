import bpy
import bmesh
from mathutils import Vector

class HERITAGE_OT_checkCurvature(bpy.types.Operator):

    bl_idname = "heritage.check_curvature"
    bl_label = "Calculate curvature"
    bl_description = "Calculate minimal and maximal mesh curvature"

    def execute(self, context):

        bm = bmesh.new()
        bm.from_mesh(bpy.context.active_object.data)

        edges = bm.edges
        edges.ensure_lookup_table()
        median = 0
        max = -2
        min = 2

        for e in edges:
            
            p1 = e.verts[0].co
            p2 = e.verts[1].co
            n1 = e.verts[0].normal
            n2 = e.verts[1].normal
            
            curva = (n2 - n1).dot(p2 - p1)
            curva = curva / (p2 - p1).length
            #print(curva)
            median += curva
            
            if curva > max: max = curva
            if curva < min: min = curva

        median = median/len(edges)
        print("Median: ", median)
        print("Max: ", max)
        print("Min: ", min)

        return {'FINISHED'}
