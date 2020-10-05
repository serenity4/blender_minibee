import bpy
from ..utils import access, exceptions
from ..blender_utils import bcollections as collections
from ...log import logger
import re
from typing import *


qcollection_number_pattern = re.compile(r"qcollection_(\d+)")

QCOLLECTION_PREFIX = 'qcollection'
QCOLLECTION_ROOT_NAME = 'Quietude'
MAKE_QCOLLECTION_ROOT_VISIBLE = True

def instance_qcollection(number):
    qcollection_root = get_qcollection_root()
    new_qcollection = bpy.data.collections.new(f'qcollection_{number}')
    new_qcollection["modifiers"] = {}
    qcollection_root.children.link(new_qcollection)
    return new_qcollection

class QCollection():

    def __init__(self):
        self.collection = QCollection.create_qcollection()

    @classmethod
    def create_qcollection(cls):
        """Creates a new qcollection, with the smallest number possible.
        """
        qcollection_root = get_qcollection_root(create_auto=True, warn=True)
        qcollections = list(qcollection_root.children.values())
        logger.debug(f"QCollections: {qcollections}")
        if not qcollections:
            return instance_qcollection(1)
        else:
            for index, number in enumerate(iter_get_qcollection_numbers()):
                logger.debug(f"Index: {index}, Number: {number}")
                if (index + 1) != number:
                    logger.debug(f"MATCH for Index: {index}, Number: {number}")
                    return instance_qcollection(index + 1)
            return instance_qcollection(number + 1)

    def populate(self, objs):
        collections.populate_collection(self.collection, objs)

def find_common_qcollection(objs):
    qcollection_root = get_qcollection_root()
    if qcollection_root:
        for qcollection in qcollection_root.children.values():
            if set(objs) == set(qcollection.objects):
                return qcollection
        

def extract_qcollection_number(qcollection_name):
    return int(re.search(qcollection_number_pattern, qcollection_name).group(1))

def get_qcollection_root(create_auto=False, warn=False):
    qcollection_root = access.get_key(QCOLLECTION_ROOT_NAME, bpy.data.collections, warn=warn)
    if not qcollection_root and create_auto:
        qcollection_root = bpy.data.collections.new(QCOLLECTION_ROOT_NAME)
        if MAKE_QCOLLECTION_ROOT_VISIBLE:
            bpy.context.scene.collection.children.link(qcollection_root)
    return qcollection_root

def get_qcollection_by_number(number):
    return get_qcollection_root().children[f"{QCOLLECTION_PREFIX}_{number}"]

def iter_find_obj_in_collections(obj):
    collections = bpy.data.collections
    for name, collection in collections.items():
        if obj in collection.objects.items():
            yield collection

def iter_find_obj_in_qcollections(obj_name):
    qcollection = get_qcollection_root()
    for subcollection in qcollection_root.children.values():
        if obj_name in subcollection.object.keys():
            yield subcollection

def iter_get_qcollection_numbers():
    qcollection_root = get_qcollection_root()
    yield from sorted(map(extract_qcollection_number, qcollection_root.children.keys()))

def get_modifier_name(qcollection, modifier_type):
    qcol_modifier_names = list(qcollection["modifiers"].keys())
    qcol_number = extract_qcollection_number(qcollection.name)
    prefix = f"Q{qcol_number}_"
    if qcol_modifier_names:
        for index, number in enumerate(map(lambda x: int(re.search(f"{modifier_type}_(\\d+)", x).group(1)), qcol_modifier_names)):
            if index + 1 != number:
                return prefix + f"{modifier_type}_{index + 1}"
        return prefix + f"{modifier_type}_{len(qcol_modifier_names)+1}"
    return prefix + f"{modifier_type}_1"

def fetch_qcollection(mesh_objs):
    qcol = find_common_qcollection(mesh_objs)
    if not qcol:
        qcol_creator = QCollection()
        qcol_creator.populate(mesh_objs)
        qcol = qcol_creator.collection
        logger.debug("Creating new qcollection.")
    return qcol