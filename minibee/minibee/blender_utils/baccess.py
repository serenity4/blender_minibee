import bpy

def iter_get_mesh_obj(objs):
    for obj in objs:
        if isinstance(obj.data, bpy.types.Mesh):
            yield obj
    