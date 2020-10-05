import bpy
from quietude.quietude.blender_utils import bcollections

def test_qcollection_root_present():
    assert(bcollections.is_collection_present('Quietude'))
    

def test_qcollections_present():
    assert(bcollections.is_collection_present('qcollection_1'))
    assert(bcollections.is_collection_present('qcollection_1')) 

def test_qcollections_children_of_root():
    qcolroot = bcollections.get_collection_by_name("Quietude")
    assert(bcollections.is_subcollection(qcolroot, 'qcollection_1'))
    assert(bcollections.is_subcollection(qcolroot, 'qcollection_2'))

def test_qcollections_fill_empty_name_slots_at_creation():
    bpy.data.objects['Cylinder'].select_set(True)
    bpy.ops.quietude.add_qcollection_modifier()
    bpy.data.collections.remove(bpy.data.collections['qcollection_2'])
    bpy.data.objects['Cylinder'].select_set(False)
    bpy.ops.quietude.add_qcollection_modifier()
    assert(bcollections.is_collection_present('qcollection_1'))
    assert(bcollections.is_collection_present('qcollection_2'))
    assert(bcollections.is_collection_present('qcollection_3'))
    assert(not bcollections.is_collection_present('qcollection_4'))