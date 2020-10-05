import bpy
from ...blender_utils import bmodifiers, baccess
from ...core import qcollections

available_modifiers = [
    ("MIRROR", "Mirror", "Mirror modifier"),
    ("ARRAY", "Array", "Array modifier"),
    ("DISPLACE", "Displace", "Displace modifier")
    ]

class AddQCollectionModifier(bpy.types.Operator):
    bl_idname = "quietude.add_qcollection_modifier"
    bl_label = "Add QCollection Modifier"
    bl_description = "Adds a QCollection modifier."
    bl_options = {"REGISTER", "UNDO"}

    modifier_type: bpy.props.EnumProperty(items=available_modifiers,
                                          name="QCollection modifiers",
                                          description="Modifiers that can be applied to a QCollection"
                                          )

    @classmethod
    def poll(cls, context):
        return context.selected_objects != []

    def execute(self, context):
        modifier_type = self.modifier_type
        objs = context.selected_objects
        mesh_objs = list(baccess.iter_get_mesh_obj(objs))
        if not mesh_objs:
            return {'FINISHED'}
        qcol = qcollections.fetch_qcollection(mesh_objs)
        modifier_name = qcollections.get_modifier_name(qcol, modifier_type)
        for index, mesh_obj in enumerate(mesh_objs):
            bmodifiers.add_modifier_to_obj(mesh_obj, modifier_type, modifier_name)
            if index == 0:
                bmodifiers.link_modifier_to_collection(modifier_type, modifier_name, qcol, mesh_obj)
            bmodifiers.drive_object_modifier_from_collection(mesh_obj, modifier_name, qcol)

        return {"FINISHED"}
