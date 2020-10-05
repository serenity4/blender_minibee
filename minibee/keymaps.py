import bpy

addon_keymaps = []

kmi_dictlist = [
    {
        'idname': "wm.call_menu_pie",
        'type': "M",
        'value': "PRESS",
        'shift': True,
        'ctrl': True,
        'alt': False,
        'oskey': False,
        'properties': {
            'name': 'VIEW3D_MT_QCollectionPieMenu'
        }
    }
]

def extract_properties(kmi_dict):
    if 'properties' in kmi_dict.keys():
            return kmi_dict.pop('properties')
    else:
        return

def set_properties(kmi, properties_dict):
    if properties_dict:
        for property_name, property_value in properties_dict.items():
            setattr(kmi.properties, property_name, property_value)

def register_keymaps():
    addon = bpy.context.window_manager.keyconfigs.addon
    if not addon: # blender run in background mode
        return
    km = addon.keymaps.new(name = "3D View", space_type = "VIEW_3D")
    for kmi_dict in kmi_dictlist:
        properties_dict = extract_properties(kmi_dict)
        kmi = km.keymap_items.new(**kmi_dict)
        set_properties(kmi, properties_dict)
        
    addon_keymaps.append(km)

def unregister_keymaps():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()