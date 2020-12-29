import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel 

class ListItem (PropertyGroup):

    name: StringProperty(

        name = "Name",
        description = "Description 1",
        default = "Untitled"

    )

    index: IntProperty(

        name = "Index",
        description = "Index of item",
        default = ""

    )

class HERITAGE_UI_List (UIList):

    def draw_item (self, context, layout, data, item, icon, active_data, active_propname, index):

        custom_icon = 'OBJECT_DATAMODE'

        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.label(text = item.name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:

            layout.aligment = 'CENTER'
            layout.label(text = "", icon = custom_icon)

class LIST_OT_NewItem(Operator):

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):

        context.scene.my_list.add()

        return{'FINISHED'}

class LIST_OT_DeleteItem(Operator):

    bl_idname = "my_list.delete_item"
    bl_label = "Delete an item"
    
    @classmethod
    def poll(cls, context):

        return context.scene.my_list

    def execute(self, context):

        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1)

        return{'FINISHED'}
