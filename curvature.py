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
        cmedian = 0
        cmax = -2
        cmin = 2

        for e in edges:
            
            p1 = e.verts[0].co
            p2 = e.verts[1].co
            n1 = e.verts[0].normal
            n2 = e.verts[1].normal
            
            curva = (n2 - n1).dot(p2 - p1)
            curva = curva / (p2 - p1).length
            #print(curva)
            cmedian += curva
            
            if curva > cmax: cmax = curva
            if curva < cmin: cmin = curva

        cmedian = cmedian/len(edges)

        bpy.context.scene['CMin'] = 1.0
        bpy.context.scene['CMax'] = 1.0
        bpy.context.scene['CMedian'] = 1.0

        bpy.types.Scene.CMin = bpy.props.FloatProperty()
        bpy.types.Scene.CMin = round(cmin, 2)
        bpy.types.Scene.CMax = bpy.props.FloatProperty()
        bpy.types.Scene.CMax = round(cmax, 2)
        bpy.types.Scene.CMedian = bpy.props.FloatProperty()
        bpy.types.Scene.CMedian = round(cmedian, 2)

        return {'FINISHED'}
