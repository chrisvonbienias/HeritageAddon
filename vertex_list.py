import bpy
import bmesh
import numpy as np

obj = bpy.context.active_object

col = obj.data.vertex_colors.active

colors = np.empty([0,4])

for c in col.data:
    
    r = round(c.color[0], 2)
    g = round(c.color[1], 2)
    b = round(c.color[2], 2)
    print(r)
    
    color = [r, g, b, 1.0]   
    colors = np.vstack((colors, color))
    
colors = np.unique(colors, axis=0)

print(colors)    