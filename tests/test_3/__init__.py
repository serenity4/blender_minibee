import bpy
bpy.ops.minibee.add_qcollection_modifier()
bpy.data.objects['Cylinder'].select_set(True)
bpy.data.objects['Cube.001'].select_set(True)
bpy.ops.minibee.add_qcollection_modifier()
bpy.ops.minibee.add_qcollection_modifier()
bpy.data.objects['Cube.001'].select_set(False)
bpy.ops.minibee.add_qcollection_modifier()