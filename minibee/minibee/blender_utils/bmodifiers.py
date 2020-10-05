from __future__ import annotations
from typing import *
import bpy
from ..utils import read
from pathlib import Path

MODIFIER_PROPERTIES = read.yaml(Path(f"{Path(__file__).parent}/mappings/modifier_properties.yml"))

def has_modifier(obj, modifier_name):
    return modifier_name in obj.modifiers

def link_modifier_to_collection(modifier_type, modifier_name, collection, template_obj):
    properties = MODIFIER_PROPERTIES[modifier_type.lower()]
    collection["modifiers"][modifier_name] = {
        key: getattr(template_obj.modifiers[modifier_name], key)
        for key in properties.keys()
    }

def drive_modifier_property_from_collection(obj, property_name, index, modifier_name, collection):
    data_path = f"[\"modifiers\"][\"{modifier_name}\"][\"{property_name}\"]"
    variable_name = property_name
    if index != -1:
        data_path += f"[{index}]"
        variable_name += f"_{index}"

    dr = obj.modifiers[modifier_name].driver_add(property_name, index)
    var = dr.driver.variables.new()
    var.name = variable_name
    var.targets[0].id_type = "COLLECTION"
    var.targets[0].id = collection
    var.targets[0].data_path = data_path
    dr.driver.expression = variable_name

def drive_object_modifier_from_collection(obj: bpy.types.Object, modifier_name, collection: bpy.types.Collection):
    for key, value in collection["modifiers"][modifier_name].items():
        if value is not None :
            if hasattr(value, '__len__'):
                for i in range(len(value)):
                    drive_modifier_property_from_collection(obj, key, i, modifier_name, collection)
            else:
                drive_modifier_property_from_collection(obj, key, -1, modifier_name, collection)

        


def add_modifier_to_obj(obj: bpy.types.Object, modifier_type: bpy.props.EnumProperty, modifier_name: str):
    mod = obj.modifiers.new(type=modifier_type, name=modifier_name)