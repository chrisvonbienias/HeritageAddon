#Addon info
bl_info = {
    "name" : "HeritageAddon",
    "author" : "Krzysztof Bieniek",
    "description" : "Addon for streamlining photogrammetry aided 3D modelling and texturing",
    "blender" : (2, 80, 0),
    "location" : "View3D",
    "category" : "Generic"
}

#Library imports
import bpy
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel 

#Classes imports
from .ui import HERITAGE_PT_panel
from .pre_treatment import HERITAGE_OT_preTreatment
from .vertex_color import HERITAGE_OT_vertexColor
from .curvature import HERITAGE_OT_checkCurvature
from .holes import HERITAGE_OT_selectHoles
from .ui_list import ListItem, HERITAGE_UL_List, LIST_OT_DeleteItem, LIST_OT_NewItem

#Clases
classes = (
    HERITAGE_PT_panel,
    HERITAGE_OT_preTreatment,
    HERITAGE_OT_vertexColor,
    HERITAGE_OT_checkCurvature,
    HERITAGE_OT_selectHoles,
    ListItem,
    HERITAGE_UL_List,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem
)

#Registration
def register():

    for cls in classes:

        bpy.utils.register_class(cls)

    bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list", default = 0)

#Unregistration
def unregister():

    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index
    
    for cls in classes:

        bpy.utils.unregister_class(cls)

    

#Registration occurs only if this is the main called file
if __name__ == "__main__":

    register()

