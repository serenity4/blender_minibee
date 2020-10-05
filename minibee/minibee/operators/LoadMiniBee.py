import bpy
from .. import blender_integration as bi
from pathlib import Path

class LoadMiniBee(bpy.types.Operator):
    bl_idname = "minibee.update_animation_data"
    bl_label = "Update animation data"
    bl_description = "Update animation data for the MiniBee."
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        mini_bee = context.scene.mb_prop_minibee
        data_file = context.scene.mb_prop_datapath
        if mini_bee.name not in bi.initial_data:
            bi.initial_data[mini_bee.name] = {
                'location': mini_bee.location.copy(),
                'rotation_quaternion': mini_bee.rotation_quaternion.copy(),
            }
        else:
            bi.restore_initial_state(mini_bee)
        bi.update(mini_bee, data_file)
        return {"FINISHED"}

class RestoreMiniBee(bpy.types.Operator):
    bl_idname = "minibee.restore_object"
    bl_label = "Restore object"
    bl_description = "Restore the object to its original state"
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        mini_bee = context.scene.mb_prop_minibee
        if mini_bee.name in bi.initial_data:
            bi.restore_initial_state(mini_bee)
            del bi.initial_data[mini_bee.name]
        return {"FINISHED"}