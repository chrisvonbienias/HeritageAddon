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
from bpy.props import *
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
from .mesh_check import *

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
    HERITAGE_OT_colorCurvature,
    HERITAGE_OT_selectHoles,
    ListItem,
    HERITAGE_UL_List,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem,
    LIST_OT_AssignObject,
    LIST_OT_RemoveObject,
    LIST_OT_ColorObjects,
    HERITAGE_OT_addMaskShader,
    HERITAGE_OT_findColorID,
    HERITAGE_OT_toggleFaceOrientation,
    HERITAGE_OT_checkMesh,
    HERIATGE_OT_toggleShinyMode
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

    bpy.types.Object.curv_data = FloatVectorProperty(name = "Curvature values", default = (0, 0, 0), 
                                                    min = -2.0, max = 2.0, precision = 0, size = 3 )
    bpy.types.Object.color_id = IntProperty(name = "Color ID", default = -1)
    bpy.types.Object.mesh_status = IntVectorProperty(name = "Mesh status", default = (0, 0), size = 2)
    bpy.types.Object.curv_status = StringProperty(name = "Curvature status", default = "N/A")
    bpy.types.Object.uv_status = StringProperty(name = "UV status", default = "N/A")
    bpy.types.Object.mesh_precision = FloatProperty(name = "Mesh precision", default = 0.0005, precision = 6, unit = 'LENGTH')

    #bmesh.types.BMEdge.curvature = FloatProperty(name = "Curvature", default = 0)

#Unregistration
def unregister():

    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index
    del bpy.types.Scene.idx
    del bpy.types.Scene.color_dict
    del bpy.types.Object.color_id
    del bpy.types.Object.curv_data
    del bpy.types.Object.mesh_status
    del bpy.types.Object.curv_status
    del bpy.types.Object.uv_status
    del bpy.types.Object.mesh_precision
    
    for cls in classes:

        bpy.utils.unregister_class(cls)

    

#Registration occurs only if this is the main called file
if __name__ == "__main__":

    register()

def colorDict():

    color_dict = defaultdict(tuple)
    i = 0
    color_dict[-1] = (1.0, 1.0, 1.0, 1.0)

    for r in range(4, -1, -1):
        for g in range(4, -1, -1):
            for b in range(4, -1, -1):

                color = (r/4.0, g/4.0, b/4.0)
                color_hsv = colorsys.rgb_to_hsv(r/4.0, g/4.0, b/4.0)

                if (color_hsv[2] == 1.0 and color != (1.0, 1.0, 1.0)):

                    color += (1.0,)
                    color_dict[i] = color
                    i += 1
    
    return color_dict
