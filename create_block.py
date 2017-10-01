import bpy
import bmesh

from mathutils import Vector, Matrix
from math import cos, sin, radians

from PIL import Image

import subprocess

import os
from glob import glob


def create_block(name):
    for ob in bpy.context.scene.objects:
        ob.select = True

    bpy.ops.object.delete()
  
    # color data
    tex = Image.open('/home/jackhasakeyboard/py/minecraft_bumpmap/i/blocks/%s.png' % name)

    val = []
    floor = 255

    for x in range(tex.size[0]):
        for y in range(tex.size[1]):
            col = sum(tex.load()[x, y][0:3]) / 3

            val.append(col)

            if (col < floor):
                floor = col
          

    # resize texture
    subprocess.call(['mkdir', '/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s' % name])
    subprocess.call(['convert', '/home/jackhasakeyboard/py/minecraft_bumpmap/i/blocks/%s.png' % name, '-scale', '10000%', '/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s/%s.png' % (name, name)])


    # load texture
    img = bpy.data.images.load('/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s/%s.png' % (name, name))


    def create_plane(i):
        # init
        bpy.ops.mesh.primitive_grid_add(x_subdivisions = 17, y_subdivisions = 17, radius = 8, location = (0, 0, 0))

        ob = bpy.context.object
        me = ob.data

        # apply_texture
        bpy.ops.object.mode_set(mode = 'EDIT')

        bm = bmesh.from_edit_mesh(me)

        bpy.ops.uv.unwrap()
        
        bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['%s.png' % name] # texture must be applied in edit mode

        # rotate, currently off kilter by 90 deg
        prev_area = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        bpy.ops.transform.rotate(value = radians(90))

        bpy.context.area.type = prev_area

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
            pos = (8, 0, 8 * -r)

        if i == 2:
            pos = (0, -8, 8 * -r)

        if i == 3:
            pos = (-8, 0, 8 * -r)

        if i == 4:
            pos = (0, 8, 8 * -r)

        bpy.context.active_object.matrix_world *= Matrix.Rotation(radians(90) * r, 4, 'Y')
        bpy.context.active_object.matrix_world *= Matrix.Rotation(radians(90) * (i - 1) * r, 4, 'X')
        bpy.context.active_object.location = pos


    def create_outer():
        for i in range(5):
            create_plane(i)


    def create_inner_plane(i):
        # init
        bpy.ops.mesh.primitive_grid_add(x_subdivisions = 17, y_subdivisions = 17, radius = 8, location = (0, 0, 0))

        ob = bpy.context.object
        me = ob.data

        bm = bmesh.new()
        bm.from_mesh(me)


        # apply material
        bpy.ops.object.mode_set(mode = 'EDIT')

        bpy.ops.uv.unwrap()
        bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['%s.png' % name] # texture must be applied in edit mode

        # rotate, currently off kilter by 90 deg
        prev_area = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        bpy.ops.transform.rotate(value = radians(90))

        bpy.context.area.type = prev_area

        bpy.ops.object.mode_set(mode = 'OBJECT')

        ob = bpy.context.object
        me = ob.data


        # extrude
        detail = bmesh.new()
        detail.from_mesh(me)

        for f, face in enumerate(detail.faces[:]):
            r = bmesh.ops.extrude_discrete_faces(detail, faces = [face])
            bmesh.ops.translate(detail, vec = (0, 0, (val[f] - floor) / 400), verts = r['faces'][0].verts)

        detail.to_mesh(me)


        # remove
        bm = bmesh.new()
        bm.from_mesh(me)

        outer = []

        for vert in bm.verts:
            if not(vert.co.x > -7 and vert.co.x < 9 and vert.co.y > -7 and vert.co.y < 7):
                outer.append(vert)

        bmesh.ops.delete(bm, geom = outer[:], context = 1)

        bm.to_mesh(me)


        # translate
        r = 0 if i == 0 else 1

        if i == 0:
            pos = (0, 0, 8 * -r)

        if i == 1:
            pos = (6, 0, 8 * -r)

        if i == 2:
            pos = (0, -6, 8 * -r)

        if i == 3:
            pos = (-6, 0, 8 * -r)

        if i == 4:
            pos = (0, 6, 8 * -r)

        bpy.context.active_object.matrix_world *= Matrix.Rotation(radians(90) * r, 4, 'Y')
        bpy.context.active_object.matrix_world *= Matrix.Rotation(radians(90) * (i + 1) * r, 4, 'X')
        bpy.context.active_object.location = pos

        bm.to_mesh(me)


    def create_inner():
        for _ in range(1, 5):
            create_inner_plane(_)


        # ring, doesn't need to be rotated. Oriented right way by default
        # init
        bpy.ops.mesh.primitive_grid_add(x_subdivisions = 17, y_subdivisions = 17, radius = 8, location = (0, 0, -16))

        ob = bpy.context.object
        me = ob.data

        bm = bmesh.new()
        bm.from_mesh(me)

        # apply material
        bpy.ops.object.mode_set(mode = 'EDIT')

        bpy.ops.uv.unwrap()
        bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['%s.png' % name] # texture must be applied in edit mode

        # rotate, currently off kilter by 90 deg
        prev_area = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        bpy.ops.transform.rotate(value = radians(90))

        bpy.context.area.type = prev_area

        bpy.ops.object.mode_set(mode = 'OBJECT')


        # remove
        bm = bmesh.new()
        bm.from_mesh(me)

        inner = []

        for vert in bm.verts:
            if vert.co.x > -6 and vert.co.x < 6 and vert.co.y > -6 and vert.co.y < 6:
                inner.append(vert)

        bmesh.ops.delete(bm, geom = inner[:], context = 1)

        bm.to_mesh(me)


        # roof
        # init
        bpy.ops.mesh.primitive_grid_add(x_subdivisions = 17, y_subdivisions = 17, radius = 8, location = (0, 0, -2))

        ob = bpy.context.object
        me = ob.data

        bm = bmesh.new()
        bm.from_mesh(me)


        # apply material
        bpy.ops.object.mode_set(mode = 'EDIT')

        bpy.ops.uv.unwrap()
        bpy.data.screens['UV Editing'].areas[1].spaces[0].image = bpy.data.images['%s.png' % name] # texture must be applied in edit mode

        # rotate, currently off kilter by 90 deg
        prev_area = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'

        bpy.ops.transform.rotate(value = radians(90))

        bpy.context.area.type = prev_area

        bpy.ops.object.mode_set(mode = 'OBJECT')


        # extrude
        detail = bmesh.new()
        detail.from_mesh(me)

        for f, face in enumerate(detail.faces[:]):
            r = bmesh.ops.extrude_discrete_faces(detail, faces = [face])
            bmesh.ops.translate(detail, vec = (0, 0, -(val[f] - floor) / 400), verts = r['faces'][0].verts)

        detail.to_mesh(me)


        # remove
        bm = bmesh.new()
        bm.from_mesh(me)

        inner = []

        for vert in bm.verts:
            if not(vert.co.x > -7 and vert.co.x < 7 and vert.co.y > -7 and vert.co.y < 7):
                inner.append(vert)

        bmesh.ops.delete(bm, geom = inner[:], context = 1)

        bm.to_mesh(me)


    create_outer()
    create_inner()
    

    # resize, Shapeways dimensions are in mm
    for ob in bpy.context.scene.objects:
        ob.select = True
        
    bpy.ops.transform.resize(value = (2, 2 , 2))


    # export
    bpy.ops.export_scene.x3d(filepath = '/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s/%s.x3d' % (name, name), axis_up = 'Y')

          
    # zip
    subprocess.call(['zip', '-j', '/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s/%s.zip' % (name, name), '/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s/%s.x3d' % (name, name), '/home/jackhasakeyboard/py/minecraft_bumpmap/o/%s/%s.png' % (name, name)]) # j flag (junk the absolute path and just use the names) required for Shapeways to be happy for some reason


# mass export
for f in glob('/home/jackhasakeyboard/py/minecraft_bumpmap/i/blocks/*.png')[:]:
    name = os.path.splitext(os.path.basename(f))[0]
  
    create_block(name)

create_block('diamond_ore')
