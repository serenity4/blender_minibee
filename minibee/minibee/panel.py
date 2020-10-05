import bpy
import importlib
import logging

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Layout Demo"
    bl_idname = "VIEW_3D_PT_custompanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "view"

    def draw(self, context):
        layout = self.layout
        logging.info('All good!')

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Complex1 Row: I want logging")