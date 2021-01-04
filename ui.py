import bpy

class HERITAGE_panel:

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Heritage"
    bl_options = {'DEFAULT_CLOSED'}


class HERITAGE_PT_panel(HERITAGE_panel, bpy.types.Panel):

    bl_idname = "HERITAGE_PT_panel"
    bl_label = "Heritage Addon"
    #bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

class HERITAGE_PT_panelPre(HERITAGE_panel, bpy.types.Panel):

    bl_parent_id = "HERITAGE_PT_panel"
    bl_label = "Pre-treatment"

    def draw(self, context):

        layout = self.layout

        layout.operator("heritage.pre_treatment", text="Pre-Treatment")

class HERITAGE_PT_panelModelling(HERITAGE_panel, bpy.types.Panel):

    bl_parent_id = "HERITAGE_PT_panel"
    bl_label = "Modelling"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        layout.operator("heritage.select_by_vertexcolor")

        layout.operator("heritage.select_holes")
        
        row = layout.row()
        row.template_list("HERITAGE_UL_List", "The_List", scene, "my_list", scene, "list_index")

        row = layout.row()
        row.operator('my_list.assign_object', text = 'Assign')
        row.operator('my_list.remove_object', text = 'Remove')

        row = layout.row()
        row.operator('my_list.new_item', text = 'New group')
        row.operator('my_list.delete_item', text  = 'Remove Group')

        layout.operator('my_list.color_objects', text = 'Color Objects')

        if scene.list_index >= 0 and scene.my_list :

            item = scene.my_list[scene.list_index]

            row = layout.row()
            row.prop(item, "name")

class HERITAGE_PT_panelAfter(HERITAGE_panel, bpy.types.Panel):

    bl_parent_id = "HERITAGE_PT_panel"
    bl_label = "Mesh checking"

    def draw(self, context):

        layout = self.layout

        layout.operator("heritage.check_curvature")

        min = "Min: " + str(bpy.types.Scene.CMin)
        max = "Max: " + str(bpy.types.Scene.CMax)
        median = "Average: " + str(bpy.types.Scene.CMedian)
        layout.label(text=min)
        layout.label(text=max)
        layout.label(text=median)



class HERITAGE_PT_panelTexture(bpy.types.Panel):

    bl_idname = "HERITAGE_PT_panelTexture"
    bl_label = "Heritage Addon"
    bl_category = "Heritage"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    #bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

        layout.operator("heritage.add_mask_shader")

        layout.operator("heritage.find_colorid")