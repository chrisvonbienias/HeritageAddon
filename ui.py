import bpy

class HERITAGE_Panel:

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Heritage"


class HERITAGE_PT_Panel(HERITAGE_Panel, bpy.types.Panel):

    bl_idname = "HERITAGE_PT_panel"
    bl_label = "Heritage Addon"

    def draw(self, context):

        layout = self.layout
        scene = context.scene

class HERITAGE_PT_PanelPre(HERITAGE_Panel, bpy.types.Panel):

    bl_parent_id = "HERITAGE_PT_panel"
    bl_label = "Pre-treatment"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        obj = context.active_object

        layout = self.layout

        layout.operator("heritage.pre_treatment", text="Pre-Treatment")
        layout.prop(obj, 'mesh_precision', text = "Precision")
        layout.prop(obj, 'mesh_adapt', text = "Adaptivity")

class HERITAGE_PT_PanelModelling(HERITAGE_Panel, bpy.types.Panel):

    bl_parent_id = "HERITAGE_PT_panel"
    bl_label = "Modelling"
    bl_options = {'DEFAULT_CLOSED'}

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

class HERITAGE_PT_PanelAfter(HERITAGE_Panel, bpy.types.Panel):

    bl_parent_id = "HERITAGE_PT_panel"
    bl_label = "Mesh checking"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        obj = context.active_object

        layout = self.layout
        row = layout.row()
        row.operator("heritage.toggle_face_orientation", text = "Toggle FO")
        row.operator("heritage.toggle_shiny_mode", text = "Toggle Shiny Mode")

        layout = self.layout
        layout.label(text = "Curvature")
        layout.alignment = 'CENTER'
        row = layout.row()
        row.operator("heritage.check_curvature", text = "Check",)
        row.operator("heritage.color_curvature", text = "Color mesh")

        min = "Min: " + str(round(obj.curv_data[0], 2))
        max = "Max: " + str(round(obj.curv_data[1], 2))
        median = "Average: " + str(round(obj.curv_data[2], 2))
        layout.label(text=min + "       " + max)

        layout = self.layout
        layout.operator("heritage.check_mesh", text = "Check mesh")
        layout.label(text = "Curvature: " + obj.curv_status)
        layout.label(text = "Non-manifold vertices: " + str(obj.mesh_status[0]))
        layout.label(text = "Flat-Shaded Faces: " + str(obj.mesh_status[1]))

class HERITAGE_PT_PanelTexture(bpy.types.Panel):

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