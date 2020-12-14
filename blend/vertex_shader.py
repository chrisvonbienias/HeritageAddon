import bpy

material = bpy.context.view_layer.objects.active.active_material
material.use_nodes = True
node_tree = material.node_tree
nodes = node_tree.nodes
links = node_tree.links

nodes.new("ShaderNodeVertexColor")

nodes.new("ShaderNodeMixRGB")
nodes[3].blend_type = 'DIFFERENCE'
nodes[3].use_clamp = True
nodes[3].inputs[0].default_value = 1

nodes.new("ShaderNodeInvert")

nodes.new("ShaderNodeMath")
nodes[5].operation = 'GREATER_THAN'

nodes.new("ShaderNodeMath")
nodes[6].operation = 'SUBTRACT'

links.new(nodes[2].outputs[0], nodes[3].inputs[1])
links.new(nodes[3].outputs[0], nodes[4].inputs[1])
links.new(nodes[3].outputs[0], nodes[6].inputs[0])
links.new(nodes[4].outputs[0], nodes[5].inputs[0])
links.new(nodes[6].outputs[0], nodes[5].inputs[1])

nodes[3].location = (200, 0)
nodes[4].location = (400, 0)
nodes[5].location = (800, 0)
nodes[6].location = (400, -200)

