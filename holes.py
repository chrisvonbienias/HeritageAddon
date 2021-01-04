import bpy

class HERITAGE_OT_selectHoles(bpy.types.Operator):

    bl_idname = "heritage.select_holes"
    bl_label = "Select holes in mesh"
    bl_description = "Selects holes in mesh"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object

    def execute(self, context):

        if bpy.context.active_object.mode != 'EDIT':
            
            bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.select_mode(type = 'VERT')
        bpy.ops.mesh.select_non_manifold()

        return {"FINISHED"}

