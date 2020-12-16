import bpy

class HERITAGE_PT_panel(bpy.types.Panel):

    bl_idname = "HERITAGE_PT_panel"
    bl_label = "Heritage Addon"
    bl_category = "Heritage"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        layout.label(text = "Algorytm do wstępnej obóbki siatki")
        layout.operator("heritage.pre_treatment", text="Pre-Treatment")

        layout.label(text="Algorytm zaznaczający vertexy o tym samym kolorze")
        layout.operator("heritage.select_by_vertexcolor")
        
        layout.label(text="Algorytm sprawdzający krzywiznę siatki")
        layout.operator("heritage.check_curvature")

        layout.label(text="Algorytm sprawdzający krzywiznę siatki")
        layout.operator("heritage.select_holes")
        