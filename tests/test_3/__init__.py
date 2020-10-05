import bpy
bpy.ops.quietude.add_qcollection_modifier()
bpy.data.objects['Cylinder'].select_set(True)
bpy.data.objects['Cube.001'].select_set(True)
bpy.ops.quietude.add_qcollection_modifier()
bpy.ops.quietude.add_qcollection_modifier()
bpy.data.objects['Cube.001'].select_set(False)
bpy.ops.quietude.add_qcollection_modifier()