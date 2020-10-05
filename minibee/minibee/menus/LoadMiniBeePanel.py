import bpy
from ..operators import LoadMiniBee

class QCollectionEditorPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "MiniBee Visualization"
    bl_idname = "VIEW3D_PT_LoadMiniBee"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Edit"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(context.scene, "mb_prop_minibee")
        col.prop(context.scene, "mb_prop_datapath")
        col.operator("minibee.update_animation_data")
        col.operator("minibee.restore_object")