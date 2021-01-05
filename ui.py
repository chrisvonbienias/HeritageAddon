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

        obj = context.active_object

        layout = self.layout
        row = layout.row()
        row.operator("heritage.toggle_face_orientation", text = "Toggle FO")

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
        layout.label(text = "Holes: " + str(obj.mesh_status[0]))
        layout.label(text = "Flat Faces: " + str(obj.mesh_status[1]))
        layout.label(text = "Density: " + str(obj.mesh_status[2]))

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