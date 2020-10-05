import bpy

class DisplayQCollectionModifierMenu(bpy.types.Operator):
    bl_idname = "quietude.display_qcollection_modifier_pie_menu"
    bl_label = "Display QCollection Modifiers"
    bl_description = "Displays the QCollection Modifier menu"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_AddQCollectionModifierPieMenu")
        return {"FINISHED"}
