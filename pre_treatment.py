import bpy

class VIEW3D_OT_preTreatment(bpy.types.Operator):

    bl_idname = "view3d.pre_treatment"
    bl_label = "Pre-Treatment"
    bl_description = "Preliminary treatment of the imported mesh"

    def execute(self, context):

        #TODO
