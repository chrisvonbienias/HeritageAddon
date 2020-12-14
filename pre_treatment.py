import bpy
import bmesh

class VIEW3D_OT_preTreatment(bpy.types.Operator):

    bl_idname = "view3d.pre_treatment"
    bl_label = "Pre-Treatment"
    bl_description = "Preliminary treatment of the imported mesh"

    def execute(self, context):

        #Enter Edit Mode
        bpy.ops.object.editmode_toggle()
        #Delete loose vertices, edges and faces
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=True)
        bpy.ops.mesh.remove_doubles(threshold=0.001)
        #Fill holes
        bpy.ops.mesh.fill_holes(sides=100)
        #Exit edit mode
        bpy.ops.object.editmode_toggle()

        #Find smallest voxel size
        findSmallestVoxel(self, context)

        voxel = 0.1 #Placeholder for real value

        #Add Remesh modifier
        bpy.ops.object.modifier_add(type="REMESH")
        bpy.context.object.modifiers["Remesh"].voxel_size = voxel

        return {"FINISHED"}


def findSmallestVoxel(self, context):

    bm = bmesh.new()
    bm.from_mesh(bpy.context.object.data)

    bm.edges.ensure_lookup_table()
    len = bm.edges[0].calc_length()
    print(bm.edges[0].verts[0])

    for e in bm.edges:
    
        curr = e.calc_length()

        if curr < len :

            len = curr

            
