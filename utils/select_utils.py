import bpy


def get_mode():
    return bpy.context.object.mode


def to_mode(new_mode):
    bpy.ops.object.mode_set(mode=new_mode, toggle=False)


def to_object():
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


def to_sculpt():
    bpy.ops.object.mode_set(mode='SCULPT', toggle=False)


def to_edit():
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)


def select_all():
    bpy.ops.object.select_all(action='SELECT')


def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')


def select_mesh():
    bpy.ops.mesh.select_all(action='SELECT')


def deselect_mesh():
    bpy.ops.mesh.select_all(action='DESELECT')


def get_active():
    return bpy.context.view_layer.objects.active


def make_active(obj):
    obj.select_set(state=True)
    bpy.context.view_layer.objects.active = obj


def select(obj):
    obj.select_set(state=True)


def deselect(obj):
    obj.select_set(state=False)


def duplicate_object():
    bpy.ops.object.duplicate_move()

def add_material():
    mat = bpy.data.materials.new(name="Material")
    obj = bpy.context.object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    obj.active_material.use_nodes = True

def map_uv():
    bpy.ops.uv.smart_project()

def remesh():
    bpy.ops.object.voxel_remesh()

def decimate(ratio):
    
    bpy.ops.mesh.decimate(ratio=ratio)
