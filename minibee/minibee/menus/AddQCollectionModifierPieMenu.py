import bpy

class AddQCollectionModifierPieMenu(bpy.types.Menu):
    # label is displayed at the center of the pie menu.
    bl_idname = "VIEW3D_MT_AddQCollectionModifierPieMenu"
    bl_label = "QCollection Modifiers"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # operator_enum will just spread all available options
        # for the type enum of the operator on the pie
        pie.operator_enum(operator="quietude.add_qcollection_modifier", property="modifier_type")
        