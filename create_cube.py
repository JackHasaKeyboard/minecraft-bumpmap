import bpy
import bmesh

from mathutils import Vector, Matrix
import math
from random import randint

from PIL import Image


# color data
tex = Image.open('/home/jackhasakeyboard/py/mc/blocks/diamond_ore.png')
    
val = []
floor = 255

for x in range(tex.size[0]):
    for y in range(tex.size[1]):
        col = sum(tex.load()[x, y][0:3]) / 3
        
        val.append(col)
        
        if (col < floor):
            floor = col

def create_plane(i):
    # init
    bpy.ops.mesh.primitive_plane_add(radius = 8, location = (0, 0, 0))

    ob = bpy.context.object 
    me = ob.data


    # apply material
    bpy.ops.mesh.uv_texture_add() # unwraps, seams are irrelevant for square texture

    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['diamond_ore.png'] # texture must be applied in edit mode

    bpy.ops.mesh.subdivide(number_cuts = 15)

    bpy.ops.object.mode_set(mode = 'OBJECT')


    # extrude
    detail = bmesh.new()
    detail.from_mesh(me)

    for f, face in enumerate(detail.faces[:]):
        r = bmesh.ops.extrude_discrete_faces(detail, faces = [face])
        bmesh.ops.translate(detail, vec = (0, 0, (val[f] - floor) / 400), verts = r['faces'][0].verts)

    detail.to_mesh(me)
 
    
    # translate
    r = 0 if i == 0 else 1

    if i == 0:
        pos = (0, 0, 8 * -r)

    if i == 1:
        pos = (0, 8, 8 * -r)

    if i == 2:
        pos = (-8, 0, 8 * -r)

    if i == 3:
        pos = (0, -8, 8 * -r)

    if i == 4:
        pos = (8, 0, 8 * -r)
    
    bpy.context.active_object.matrix_world *= Matrix.Rotation(math.radians(90) * r, 4, 'X')
    bpy.context.active_object.matrix_world *= Matrix.Rotation(math.radians(90) * (i + 1) * r, 4, 'Y')
    bpy.context.active_object.location = pos
 
    
def create_cube():
    for i in range(5):
      create_plane(i)
      
    # thickness
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, -8), radius = 8)

    bpy.ops.object.mode_set(mode = 'EDIT')

    inner = bpy.context.edit_object
    data = inner.data

    bm = bmesh.from_edit_mesh(data)

    bmesh.ops.delete(bm, geom = bm.faces[4:5], context = 5)  

    bmesh.update_edit_mesh(data, True)

    bpy.ops.object.modifier_add(type = 'SOLIDIFY')
    bpy.context.object.modifiers['Solidify'].thickness = 2
    bpy.context.object.modifiers['Solidify'].use_even_offset = True
    

create_cube()
