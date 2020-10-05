import bpy
from .. import blender_integration
from pathlib import Path

class LoadMiniBee(bpy.types.Operator):
    bl_idname = "minibee.update_animation_data"
    bl_label = "Update MiniBee animation data"
    bl_description = "Update animation data for the MiniBee."
    bl_options = {"REGISTER", "UNDO"}
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        mini_bee = context.scene.mb_prop_minibee
        data_file = context.scene.mb_prop_datapath
        blender_integration.initial_data[mini_bee.name] = {
            'location': mini_bee.location.copy(),
            'rotation_quaternion': mini_bee.rotation_quaternion.copy(),
        }
        # mini_bee = blender_integration.find_mini_bee(self.mini_bee_name)
        # data_file = Path(str(Path.home()) + "/.julia/dev/MiniBee/mini_bee_data.json")
        blender_integration.update(mini_bee, data_file)
        return {"FINISHED"}