import bpy
import bmesh
import numpy as np

class HERITAGE_OT_addMaskShader(bpy.types.Operator):

    bl_idname = "heritage.add_mask_shader"
    bl_label = "Add Masking Shader"
    bl_description = "Adds a masking shader to node tree"

    @classmethod
    def poll(cls, context):

        return bpy.context.active_object and bpy.context.view_layer.objects.active.active_material


    def execute(self, context):

        vertexShader(self, context)

        return{'FINISHED'}

class HERITAGE_OT_findColorID(bpy.types.Operator):

    bl_idname = "heritage.find_colorid"
    bl_label = "Auto-masking"
    bl_description = "Adds a masking shader for each colorId in mesh"

    @classmethod
    def poll(cls, context):

        return bpy.context.view_layer.objects.active.active_material

    def execute(self, context):

        obj = bpy.context.active_object
        material = bpy.context.view_layer.objects.active.active_material
        material.use_nodes = True
        node_tree = material.node_tree
        nodes = node_tree.nodes
        links = node_tree.links
        y = 300
        x = -500

        colors = vertexList(obj)

        status = False
        for n in nodes:

            if n.name == 'Vertex Color':

                status = True
                vnode = n
                x += 400

        for c in colors:

            if status == False:

                nodes.new("ShaderNodeVertexColor")
                vnode = nodes[-1]
                vnode.location = (x, y)
                x += 400

                status = True

            vertexShader(self, context)
            nodes[-1].inputs[1].default_value = c
            links.new(vnode.outputs[0], nodes[-1].inputs[0])  
            nodes[-1].location = (x, y)
            nodes[-1].use_custom_color = True
            nodes[-1].color = c[0:3]

            y -= 200

        return{'FINISHED'}

def vertexList(obj):

    col = obj.data.vertex_colors.active

    colors = np.empty([0,4])

    for c in col.data:
        
        r = round(c.color[0], 2)
        g = round(c.color[1], 2)
        b = round(c.color[2], 2)
        
        color = [r, g, b, 1.0]   
        colors = np.vstack((colors, color))
        
    colors = np.unique(colors, axis=0)

    return colors

def vertexShader(self, context):

    bpy.ops.node.select_all(action='DESELECT')

    material = bpy.context.view_layer.objects.active.active_material
    material.use_nodes = True
    node_tree = material.node_tree
    nodes = node_tree.nodes
    i = len(nodes)
    links = node_tree.links

    nodes.new("ShaderNodeMixRGB")
    nodes[i].blend_type = 'DIFFERENCE'
    nodes[i].use_clamp = True
    nodes[i].inputs[0].default_value = 1

    nodes.new("ShaderNodeInvert")

    nodes.new("ShaderNodeMath")
    nodes[i+2].operation = 'GREATER_THAN'

    nodes.new("ShaderNodeMath")
    nodes[i+3].operation = 'SUBTRACT'
    nodes[i+3].inputs[0].default_value = 1.0
    nodes[i+3].inputs[1].default_value = 0.01

    nodes.new("ShaderNodeBrightContrast")

    nodes.new("ShaderNodeMath")
    nodes[i+5].operation = 'SUBTRACT'
    nodes[i+5].inputs[1].default_value = 1.0

    links.new(nodes[i].outputs[0], nodes[i+1].inputs[1])
    links.new(nodes[i+1].outputs[0], nodes[i+2].inputs[0])
    links.new(nodes[i+3].outputs[0], nodes[i+2].inputs[1])
    links.new(nodes[i+2].outputs[0], nodes[i+4].inputs[0])
    links.new(nodes[i+5].outputs[0], nodes[i+4].inputs[1])

    nodes[i].location = (200, 0)
    nodes[i+1].location = (400, 0)
    nodes[i+2].location = (600, 0)
    nodes[i+3].location = (400, -200)
    nodes[i+4].location = (800, 0)
    nodes[i+5].location = (500, -400)

    bpy.ops.node.group_make()

    node_groups = bpy.data.node_groups
    j = len(node_groups)
    node_group = node_groups[j-1]
    g_links = node_group.links
    g_nodes = node_group.nodes
    
    g_nodes[6].outputs.new("Color4f", "Vertex Color")
    g_nodes[6].outputs.new("Color4f", "Target Color")
    g_nodes[6].outputs.new("int", "Brightness")
    g_nodes[6].outputs.new("int", "Tolerance")
    
    g_links.new(g_nodes[6].outputs[0], g_nodes[0].inputs[1])
    g_links.new(g_nodes[6].outputs[1], g_nodes[0].inputs[2])
    g_links.new(g_nodes[6].outputs[2], g_nodes[5].inputs[0])
    g_links.new(g_nodes[6].outputs[3], g_nodes[3].inputs[1])
    g_links.new(g_nodes[4].outputs[0], g_nodes[7].inputs[0])
    
    node_group.inputs[0].name = "Vertex Color"
    node_group.inputs[1].name = "Target Color"
    node_group.inputs[2].name = "Strength"
    node_group.inputs[2].min_value = 0
    node_group.inputs[2].max_value = 1.0
    node_group.inputs[2].default_value = 1.0
    node_group.inputs[3].name = "Tolerance"
    node_group.inputs[2].default_value = 0.01
    
    bpy.ops.node.group_edit(exit=False)

    nodes[-1].width = 200
    nodes[-1].label = "Vertex Color Mask"