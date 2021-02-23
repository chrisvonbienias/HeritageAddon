import bpy
from bpy.props import StringProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel 

class ListItem (PropertyGroup):

    name: StringProperty(

        name = "Name",
        description = "Name of the material",
        default = "Material"

    )

    idx: IntProperty (

        name = "ID",
        default = 0
    )

class HERITAGE_UL_List (UIList):

    def draw_item (self, context, layout, data, item, icon, active_data, active_propname, index):

        custom_icon = 'OBJECT_DATA'

        split = layout.split(factor=0.3)
        split.label(text = "ID: %i" % (item.idx))
        split.label(text = item.name, icon = custom_icon)


class LIST_OT_NewItem (Operator):

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    @classmethod
    def poll(cls, context):

        return len(context.scene.my_list) <= len(context.scene.color_dict) - 2

    def execute(self, context):

        id_list = []
        col_list = list(context.scene.color_dict.keys())
        col_list.pop(0)

        for l in context.scene.my_list:
            
            id_list.append(l.idx)

        diff = list(list(set(id_list) - set(col_list)) + list(set(col_list) - set(id_list)))

        context.scene.my_list.add()

        if not context.scene.my_list:

            context.scene.idx = 0

        else:

            index = min(diff)

        context.scene.my_list[-1].idx = index
        context.scene.my_list[-1].name = "Material " + str(index)

        return{'FINISHED'}

class LIST_OT_DeleteItem (Operator):

    bl_idname = "my_list.delete_item"
    bl_label = "Delete an item"
    
    @classmethod
    def poll(cls, context):

        return context.scene.my_list and context.mode == 'OBJECT'

    def execute(self, context):

        my_list = context.scene.my_list
        index = bpy.context.scene.list_index
        objects = context.scene.objects
        selected = list(filter(lambda o: o.type == 'MESH', objects))

        for obj in selected:

            if obj.color_id == index:

                obj.color_id = -1

        my_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1)
        bpy.ops.my_list.color_objects()

        return{'FINISHED'}

class LIST_OT_AssignObject (Operator):

    bl_idname = "my_list.assign_object"
    bl_label = "Assign"

    @classmethod
    def poll(cls, context):

        return context.scene.my_list and bpy.context.selected_objects and context.active_object.type == 'MESH'

    def execute(self, context):

        objects = context.scene.objects
        selected = list(filter(lambda o: o.select_get(), objects))
        index = context.scene.list_index

        for obj in selected:

            obj.color_id = index

        return {'FINISHED'}

class LIST_OT_RemoveObject (Operator):

    bl_idname = "my_list.remove_object"
    bl_label = "Remove"

    @classmethod
    def poll(cls, context):

        return context.scene.my_list and bpy.context.selected_objects and context.active_object.type == 'MESH'

    def execute(self, context):

        objects = context.scene.objects
        selected = list(filter(lambda o: o.select_get(), objects))

        for obj in selected:

            obj.color_id = -1

        return {'FINISHED'}

class LIST_OT_ColorObjects (Operator):

    bl_idname = "my_list.color_objects"
    bl_label = "Assign colors to objects"

    @classmethod
    def poll(cls, context):

        return context.mode == 'OBJECT'
        
    def execute(self, context):

        objects = context.scene.objects
        selected = list(filter(lambda o: o.type == 'MESH', objects))
        color_dict = bpy.types.Scene.color_dict

        for obj in selected:

            color_id = obj.color_id
            color = color_dict[color_id]

            if not ('Masking' in obj.data.vertex_colors.keys()):

                obj.data.vertex_colors.new(name = 'Masking')
                obj.data.vertex_colors['Masking'].active = True

            color_layer = obj.data.vertex_colors.active

            for poly in obj.data.polygons:
                for loop in poly.loop_indices:

                    color_layer.data[loop].color = color

        bpy.context.space_data.shading.color_type = 'VERTEX'

        return {'FINISHED'}