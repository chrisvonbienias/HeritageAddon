import bpy
import bmesh
from mathutils import Vector
from collections import defaultdict
import numpy as np
import colorsys

class HERITAGE_OT_CheckCurvature(bpy.types.Operator):

    bl_idname = "heritage.check_curvature"
    bl_label = "Calculate curvature"
    bl_description = "Calculate minimal and maximal mesh curvature"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object

    def execute(self, context):

        obj = bpy.context.active_object
        bm = bmesh.new()
        bm.from_mesh(obj.data)

        edges = bm.edges
        edges.ensure_lookup_table()
        cmedian = 0
        cmax = -10
        cmin = 10

        for e in edges:
            
            p1 = e.verts[0].co
            p2 = e.verts[1].co
            n1 = e.verts[0].normal
            n2 = e.verts[1].normal
            
            curva1 = 2 * n1.dot(p1 - p2)
            curva2 = 2 * n2.dot(p2 - p1)

            if not (p1 - p2).length :
                curva1 = curva1 / (p1 - p2).length

            if not (p2 - p1).length :
                curva2 = curva2 / (p2 - p1).length

            curva1 = round(curva1, 3)
            curva2 = round(curva2, 3)
            
            if max(curva1, curva2) > cmax: cmax = max(curva1, curva2)
            if min(curva1, curva2) < cmin: cmin = min(curva1, curva2)

        #cmedian = cmedian/len(edges)

        obj.curv_data[0] = round(cmin, 2)
        obj.curv_data[1] = round(cmax, 2)
        #obj.curv_data[2] = round(cmedian, 2)

        return {'FINISHED'}

class HERITAGE_OT_ColorCurvature(bpy.types.Operator):

    bl_idname = "heritage.color_curvature"
    bl_label = "Color curvature"
    bl_description = "Color mesh with curvature data"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object

    def execute(self, context):

        obj = bpy.context.active_object.data
        bm = bmesh.new()
        bm.from_mesh(obj)

        if not ('Curvature' in obj.vertex_colors.keys()):

            obj.vertex_colors.new(name = 'Curvature')
            obj.vertex_colors['Curvature'].active = True

        col = obj.vertex_colors['Curvature']
        col.active = True

        edges = bm.edges
        faces = bm.faces
        verts = bm.verts
        verts.ensure_lookup_table()
        faces.ensure_lookup_table()
        edges.ensure_lookup_table()

        verts_dict = defaultdict(list)
        vertex_map = defaultdict(list)

        for f in faces:
            for v_ix, l_ix in zip(f.verts, f.loops):
                vertex_map[v_ix.index].append(l_ix)

        for e in edges:
            
            v1 = e.verts[0]
            v2 = e.verts[1]
            p1 = v1.co
            p2 = v2.co
            n1 = v1.normal
            n2 = v2.normal
            
            curva1 = 2 * n1.dot(p1 - p2)
            curva2 = 2 * n2.dot(p2 - p1)

            if (p1 - p2).length :
                curva1 = curva1 / (p1 - p2).length

            if (p2 - p1).length :
                curva2 = curva2 / (p2 - p1).length

            curva1 = round(curva1, 3)
            curva2 = round(curva2, 3)
            
            #Add v1
            verts_dict[v1.index].append([e.index, abs(curva1)])
            #Add v2
            verts_dict[v2.index].append([e.index, abs(curva2)])

        for v, edge in verts_dict.items():

            average = 0
            for e in edge:

                average += e[1]

            average /= len(edge)

            h = np.interp(average, [0, 1.0], [0.333, 0])
            color = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            color += (1.0,)

            for l in vertex_map[v]:

                col.data[l.index].color = color

        return {'FINISHED'}
