import bpy

class HERITAGE_PT_panel(bpy.types.Panel):

    bl_label = "Heritage Addon"
    bl_category = "Heritage"
    bl_space_type = "View3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        layout.label(text = "TEST")