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
import colorsys

#Classes imports
from .ui import *
from .pre_treatment import *
from .vertex_color import *
from .curvature import *
from .holes import *
from .ui_list import *
from .vertex_shader import *

#Clases
classes = (
    HERITAGE_PT_panel,
    HERITAGE_PT_panelTexture,
    HERITAGE_PT_panelPre,
    HERITAGE_PT_panelModelling,
    HERITAGE_PT_panelAfter,
    HERITAGE_OT_preTreatment,
    HERITAGE_OT_vertexColor,
    HERITAGE_OT_checkCurvature,
    HERITAGE_OT_selectHoles,
    ListItem,
    HERITAGE_UL_List,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem,
    LIST_OT_AssignObject,
    LIST_OT_RemoveObject,
    LIST_OT_ColorObjects,
    HERITAGE_OT_addMaskShader,
    HERITAGE_OT_findColorID
)

#Registration
def register():

    for cls in classes:

        bpy.utils.register_class(cls)

    bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.idx = IntProperty(name = "ID", default = 0)
    color_dict = colorDict()
    bpy.types.Scene.color_dict = color_dict

    bpy.types.Scene.CMin = 0
    bpy.types.Scene.CMax = 0
    bpy.types.Scene.CMedian = 0

    bpy.types.Object.color_id = IntProperty(name = "Color ID", default = 0)

#Unregistration
def unregister():

    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index
    
    for cls in classes:

        bpy.utils.unregister_class(cls)

    

#Registration occurs only if this is the main called file
if __name__ == "__main__":

    register()

def colorDict():

    color_dict = defaultdict(tuple)
    i = 0
    color_dict[-1] = (1.0, 1.0, 1.0, 1.0)

    for r in range(2, -1, -1):
        for g in range(2, -1, -1):
            for b in range(2, -1, -1):

                color = (r/2.0, g/2.0, b/2.0)
                color_hsv = colorsys.rgb_to_hsv(r/2.0, g/2.0, b/2.0)

                if (color_hsv[2] == 1.0 and color != (1.0, 1.0, 1.0)):

                    color += (1.0,)
                    color_dict[i] = color
                    i += 1
    
    return color_dict
