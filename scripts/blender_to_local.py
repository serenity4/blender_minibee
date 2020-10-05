from pathlib import Path
import shutil

ADDON = 'quietude'

def main():
    addon_blender_path = Path(f"./external/blender-2.82/2.82/scripts/addons/{ADDON}")
    addon_github_path = Path(f"./{ADDON}")
    if addon_github_path.exists():
        shutil.rmtree(addon_github_path)
    shutil.copytree(addon_blender_path, addon_github_path)


if __name__ == '__main__':
    main()