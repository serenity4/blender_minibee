import bpy

def test_modifier_is_present_on_collection():
    objects = ['Cube', 'Cube.001']
    assert(all([list(bpy.data.objects[obj].modifiers.keys()) for obj in objects]))
