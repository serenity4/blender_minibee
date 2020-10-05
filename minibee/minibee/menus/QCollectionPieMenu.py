import bpy

class QCollectionPieMenu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_QCollectionPieMenu"
    bl_label = "QCollection menu."

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator('quietude.display_qcollection_modifier_pie_menu', text="Add QCollection Modifier")
        