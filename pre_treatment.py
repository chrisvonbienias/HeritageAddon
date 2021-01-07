import bpy
import bmesh

class HERITAGE_OT_preTreatment(bpy.types.Operator):

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
        merge_limit = obj.merge_limit
        voxel_limit = obj.voxel_limit

        if not merge_limit:
            merge_limit = 0.01

        #Enter Edit Mode
        bpy.ops.object.editmode_toggle()
        #Delete loose vertices, edges and faces
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
        bpy.ops.mesh.remove_doubles(threshold=merge_limit)
        #Fill holes
        bpy.ops.mesh.fill_holes(sides=100)
        #Exit edit mode
        bpy.ops.object.editmode_toggle()

        #Find smallest voxel size
        if not voxel_limit:
            voxel = findSmallestVoxel(self, context)
        else:
            voxel = voxel_limit

        #Add Remesh modifier
        bpy.ops.object.modifier_add(type = 'REMESH')
        mods["Remesh"].voxel_size = voxel
        
        return {"FINISHED"}


def findSmallestVoxel(self, context):

    bm = bmesh.new()
    bm.from_mesh(bpy.context.active_object.data)

    bm.edges.ensure_lookup_table()
    len = bm.edges[0].calc_length()

    for e in bm.edges:
    
        curr = e.calc_length()

        if curr < len :

            len = curr

    return len

def getSceneFaces(self, context):

    view_layer = context.scene.view_layers['View Layer']
    stats = context.scene.statistics(view_layer)

    stat_list = stats.split(' | ')
    faces = stat_list[3]
    faces = faces.split(':')
    faces = int(faces[1])

    return faces
