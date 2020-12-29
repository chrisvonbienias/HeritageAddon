import bpy

class HERITAGE_PT_panel(bpy.types.Panel):

    bl_idname = "HERITAGE_PT_panel"
    bl_label = "Heritage Addon"
    bl_category = "Heritage"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        layout.label(text = "Algorytm do wstępnej obóbki siatki")
        layout.operator("heritage.pre_treatment", text="Pre-Treatment")

        layout.label(text="Algorytm zaznaczający vertexy o tym samym kolorze")
        layout.operator("heritage.select_by_vertexcolor")
        
        layout.label(text="Algorytm sprawdzający krzywiznę siatki")
        layout.operator("heritage.check_curvature")

        layout.label(text="Algorytm zaznaczający dziury")
        layout.operator("heritage.select_holes")
        
        row = layout.row()
        row.template_list("HERITAGE_UL_List", "The_List", scene, "my_list", scene, "list_index")

        row = layout.row()
        row.operator('my_list.new_item', text = 'NEW')
        row.operator('my_list.delete_item', text  = 'REMOVE')

        if scene.list_index >= 0 and scene.my_list :

            item = scene.my_list[scene.list_index]

            row = layout.row()
            row.prop(item, "name")
        