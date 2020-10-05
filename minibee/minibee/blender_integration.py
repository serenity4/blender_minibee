"""Integrates simulation data onto a Blender model.
"""


import numpy as np
import bpy
from mathutils import *
from ..log import logger
from .utils.read import json, convert_dict_list_to_array
from pathlib import Path
import importlib


def update_mini_bee(mini_bee, data):
    # Loops over all time steps and keyframes the result to the mini-bee (location + rotation).
    mini_bee.animation_data_clear()
    restore_initial_state(mini_bee)
    FPS = bpy.context.scene.render.fps
    for i in range(data['attitude'].shape[0]):
        frame = FPS*data['time'][i]
        mini_bee.location = data['position'][i, :]
        mini_bee.rotation_quaternion = data['attitude'][i, :]
        mini_bee.rotation_quaternion /= np.linalg.norm(mini_bee.rotation_quaternion)
        # quat = Quaternion(data['attitude'][i, :] / np.linalg.norm(data['attitude'][i, :]))
        # mini_bee.rotation_euler = initial_data['rotation_euler'].copy()
        # mini_bee.rotation_euler.rotate(quat)
        # __import__('code').interact(local={k: v for ns in (globals(), locals()) for k, v in ns.items()})
        mini_bee.keyframe_insert(data_path='location',
                                frame=frame)
        mini_bee.keyframe_insert(
            data_path='rotation_quaternion', frame=frame)

def find_mini_bee(mini_bee_name):
    # Lists the objects and extracts the obstacles and the mini-bee
    mini_bee = None
    # importlib.reload(bpy)
    for obj in bpy.data.objects:
        if obj.name == mini_bee_name:
            mini_bee = obj
            logger.info(f"Found MiniBee object {obj}")
            
        # if "Obstacle" in obj.name or "Terrain" in obj.name:
        #     print("Obstacle: {}".format(obj.name))
        #     obstacles.append(obj)
    if mini_bee_name not in initial_data:
        initial_data[mini_bee_name] = {
            'location': mini_bee.location.copy(),
            'rotation_quaternion': mini_bee.rotation_quaternion.copy(),
        }
    return mini_bee

initial_data = {}


def restore_initial_state(mini_bee):
    mini_bee.animation_data_clear()
    data = initial_data[mini_bee.name]
    mini_bee.location = data["location"]
    mini_bee.rotation_quaternion = data["rotation_quaternion"]


def update(mini_bee, data_file):
    data = convert_dict_list_to_array(json(data_file))
    update_mini_bee(mini_bee, data)

#
# terrain = {}
#
# for ob in obstacles:
#     terrain[ob.name] = {}
#     print("obj: {}".format(ob.name))
#     vertex_list = []
#     for i in range(len(ob.data.vertices)):
#         vertex_positions = ob.matrix_world @ ob.data.vertices[i].co
#         vertex_positions = [*vertex_positions] # convert "vector" type to list
#         vertex_list.append(vertex_positions)
#     terrain[ob.name]['vertices'] = vertex_list
#
# print(terrain)
#
# with open(output_json, 'w') as ofile:
#     json.dump(terrain, ofile)
