import os
import sys
import zipfile
import shutil
import bpy
from pathlib import Path


def zip_target(target, target_location):
    if target_location is None:
        target_location = target + ".zip"
    zf = zipfile.ZipFile(target_location, "w")
    if os.path.isdir(target):
        for dirname, subdirs, files in os.walk(target):
            zf.write(dirname)
            for filename in files:
                zf.write('/'.join((dirname, filename)))
    else:
        zf.write(target)
    zf.close()


def install_addon(addon_name):
    source_location = addon_name
    zip_location = source_location + ".zip"
    if os.path.exists(zip_location):
        os.remove(zip_location)

    zip_target(source_location, zip_location)
    bpy.ops.preferences.addon_install(overwrite=True, filepath=os.path.abspath(zip_location))
    bpy.ops.preferences.addon_enable(module=addon_name)
    os.remove(zip_location)


def disable(addon_name):
    bpy.ops.preferences.addon_disable(module=addon_name)


def get_addon_path(addon_name):
    script_path = bpy.utils.script_paths("addons")[0]
    return Path(f"{script_path}/{addon_name}")


def get_version(addon_name):
    mod = sys.modules[addon_name]
    return mod.bl_info.get("version", (-1, -1, -1))
