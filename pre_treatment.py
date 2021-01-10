import bpy
import bmesh

class HERITAGE_OT_PreTreatment(bpy.types.Operator):

    bl_idname = "heritage.pre_treatment"
    bl_label = "Pre-Treatment"
    bl_description = "Preliminary treatment of the imported mesh"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object.type == 'MESH' and context.mode == 'OBJECT'
        
    def execute(self, context):

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        obj = context.active_object
        mods = obj.modifiers
        prec = obj.mesh_precision

        #Enter Edit Mode
        bpy.ops.object.editmode_toggle()
        #Delete loose vertices, edges and faces
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
        bpy.ops.mesh.remove_doubles(threshold=prec)
        #Fill holes
        bpy.ops.mesh.fill_holes(sides=1000)
        #Exit edit mode
        bpy.ops.object.editmode_toggle()

        #Find smallest voxel size
        if not prec:
            voxel, adapt = findSmallestVoxel(self, context)
            
        else:
            voxel = prec
            adapt = 0

        if voxel < prec:
            voxel = prec

        if not obj.mesh_adapt:
            adapt = 0

        #Add Remesh modifier
        bpy.ops.object.modifier_add(type = 'REMESH')
        mods["Remesh"].voxel_size = voxel
        mods["Remesh"].adaptivity = adapt
        
        return {"FINISHED"}


def findSmallestVoxel(self, context):

    bm = bmesh.new()
    bm.from_mesh(bpy.context.active_object.data)
    bm.edges.ensure_lookup_table()
    length = bm.edges[0].calc_length()
    adapt = 0

    for e in bm.edges:
    
        curr = e.calc_length()
        if curr < length : length = curr
        if curr > adapt : adapt = curr

    return length, adapt

def getSceneFaces(self, context):

    view_layer = context.scene.view_layers['View Layer']
    stats = context.scene.statistics(view_layer)

    stat_list = stats.split(' | ')
    faces = stat_list[3]
    faces = faces.split(':')
    faces = int(faces[1])

    return faces
