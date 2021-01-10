import bpy

class HERITAGE_OT_SelectHoles(bpy.types.Operator):

    bl_idname = "heritage.select_holes"
    bl_label = "Select holes in mesh"
    bl_description = "Selects holes in mesh"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object and context.mode == 'EDIT_MESH'

    def execute(self, context):

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(type = 'VERT')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.mesh.select_mode(type = 'EDGE')

        return {"FINISHED"}

