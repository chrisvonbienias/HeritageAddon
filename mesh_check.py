import bpy
import bmesh

class HERITAGE_OT_ToggleFaceOrientation (bpy.types.Operator):

    bl_idname = "heritage.toggle_face_orientation"
    bl_label = "Toggle face orientation"
    bl_description = "Toggles face orientation overlay"

    def execute(self, context):

        for area in context.screen.areas:

            if area.type == 'VIEW_3D':

                for space in area.spaces:

                    if space.type == 'VIEW_3D':

                        space.overlay.show_face_orientation = not space.overlay.show_face_orientation

                        break

        return {'FINISHED'}

class HERIATGE_OT_ToggleShinyMode(bpy.types.Operator):

    bl_idname = "heritage.toggle_shiny_mode"
    bl_label = "Toggle face orientation"
    bl_description = "Toggles face orientation overlay"

    def execute(self, context):

        if bpy.context.space_data.shading.light == 'STUDIO':

            bpy.context.space_data.shading.light = 'MATCAP'
            bpy.context.space_data.shading.studio_light = 'metal_carpaint.exr'

        else:

            bpy.context.space_data.shading.light = 'STUDIO'
    
        return {'FINISHED'}


class HERITAGE_OT_CheckMesh(bpy.types.Operator):

    bl_idname = "heritage.check_mesh"
    bl_label = "Check mesh"
    bl_description = "Analyze mesh for problems"

    @classmethod
    def poll(cls, context):

        return context.active_object and context.mode == 'OBJECT'

    def execute(self, context):

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        obj = context.active_object
        
        # Hole check
        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(type = 'VERT')
        bpy.ops.mesh.select_non_manifold()

        bpy.ops.object.editmode_toggle()

        verts = obj.data.vertices
        selected = list(filter(lambda v: v.select, verts))

        obj.mesh_status[0] = len(selected)

        # Curvature check
        bpy.ops.heritage.check_curvature()
        cmin = obj.curv_data[0]
        cmax = obj.curv_data[1]

        if cmin >= -1.0 and cmax <= 1.0:

            obj.curv_status = "OK"

        else:

            obj.curv_status = "Too high"

        # Flat faces check
        faces = obj.data.polygons

        selected = list(filter(lambda f: f.use_smooth == False, faces))

        obj.mesh_status[1] = len(selected)

        return {'FINISHED'}
