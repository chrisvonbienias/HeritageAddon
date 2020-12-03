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

#Classes imports
from .ui import HERITAGE_PT_panel
from .pre_treatment import VIEW3D_OT_preTreatment
from .vertex_color import VIEW3D_OT_vertexColor

#Clases
classes = (
    HERITAGE_PT_panel,
    VIEW3D_OT_preTreatment,
    VIEW3D_OT_vertexColor
)

#Registration
def register():

    for cls in classes:

        bpy.utils.register_class(cls)

#Unregistration
def unregister():

    for cls in classes:

        bpy.utils.unregister_class(cls)

#Registration occurs only if this is the main called file
if __name__ == "__main__":

    register()

