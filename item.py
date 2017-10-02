import bpy
import bmesh

from math import cos, sin, radians

from PIL import Image


cwd = bpy.path.abspath('//')

name = 'diamond'

# load texture
img = bpy.data.images.load('%s/i/items/%s.png' % (cwd, name))


# color data
tex = Image.open('%s/i/items/%s.png' % (cwd, name))
    

def create_side(s):
    # create
    # init
    bpy.ops.mesh.primitive_grid_add(x_subdivisions = 17, y_subdivisions = 17, radius = 8, location = (0, 0, 0))

    ob = bpy.context.object
    me = ob.data


    # apply texture
    bpy.ops.object.mode_set(mode = 'EDIT')

    bpy.ops.uv.unwrap()
    bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['%s.png' % name] # texture must be applied in edit mode

    # rotate, currently off-kilter by 180 deg
    prev_area = bpy.context.area.type
    bpy.context.area.type = 'IMAGE_EDITOR'

    bpy.ops.transform.rotate(value = radians(180))

    # make inverse on x axis, indexing of faces is off
    bpy.ops.transform.resize(value = (-1, 1, 1))

    bpy.context.area.type = prev_area

    bpy.ops.object.mode_set(mode = 'OBJECT')


    # remove
    bm = bmesh.new()
    bm.from_mesh(me)

    missing = []

    bm.faces.ensure_lookup_table()

    for (i, pixel) in enumerate(list(tex.getdata())):
      alpha = pixel[3]
      
      if (alpha == 0):
        missing.append(bm.faces[i])
        
    bmesh.ops.delete(bm, geom = missing, context = 5)

    bm.to_mesh(me)


    # bump
    bm = bmesh.new()
    bm.from_mesh(me)

    floor = 255

    for face in bm.faces[:]:
        bm.faces.ensure_lookup_table()
        
        i = face.index
        
        pix = tex.getdata()[i]
        
        val = sum(pix[0:2]) / 3
        
        if (val < floor):
          floor = val
        
        
        r = bmesh.ops.extrude_discrete_faces(bm, faces = [face])
        bmesh.ops.translate(bm, vec = (0, 0, (val - floor) / 400), verts = r['faces'][0].verts)

    bm.to_mesh(me)


    # thicken
    bm = bmesh.new()
    bm.from_mesh(me)
    print(-s)

    for (f, face) in enumerate(tex.getdata()):
        bm.faces.ensure_lookup_table()
      
        r = bmesh.ops.extrude_discrete_faces(bm, faces = [bm.faces[f]])
        bmesh.ops.translate(bm, vec = (0, 0, 0.5 * -s), verts = r['faces'][0].verts)

    bm.to_mesh(me)
    

for _ in range(2):
  create_side(_)
