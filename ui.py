import bpy

class HERITAGE_PT_panel(bpy.types.Panel):

    bl_label = "Heritage Addon"
    bl_category = "Heritage"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        layout.label(text = "Algorytm do wstępnej obóbki siatki")
        row = layout.row()
        row.operator("view3d.pre_treatment", text="Pre-Treatment")

        layout.label(text="Algorytm zaznaczający vertexy o tym samym kolorze")
        
        