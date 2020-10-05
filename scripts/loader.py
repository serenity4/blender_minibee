import os
import sys
import argparse
import pytest
import shutil
from pathlib import Path

try:
    sys.path.append(os.environ["LOCAL_PYTHONPATH"])
    import addon_helper
except Exception as e:
    print(e)
    sys.exit(1)

ADDON = "quietude"


def parse_cli():
    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', type=int, default=0, help="Runs the test corresponding to the provided number and exits. No tests are run for a value of zero (default).")
    parser.add_argument('--install', action='store_true', help="Installs the addon (zips it and imports it from within Blender). No effect is the addon is already installed, unless called with --override.")
    parser.add_argument('--override', action='store_true', help='Overrides existing addon, if one has already been installed.')
    parser.add_argument('--bversion', type=str, default='2.82', help="Blender version.")
    args = parser.parse_args(argv)
    return args.test, args.install, args.override, args.bversion


def run_pytest(test_number):
    test_dirs = [item for item in os.listdir("tests") if item.startswith("test_")]
    python_files = [Path(f"tests/{test_dir}/{test_file}") for test_dir in test_dirs for test_file in os.listdir(f"tests/{test_dir}") if test_file.endswith('.py')]
    ignore_flags = [f"--ignore={python_file}" for python_file in python_files if python_file.parent.name != f"test_{test_number}"]
    if not test_dirs or len(ignore_flags) == len(python_files):
        print(f"No python test files detected for test_number {test_number}.")
        sys.exit(-1)
    pytest_flags = ["tests", "-v", *ignore_flags]
    print(f"pytest {pytest_flags}")
    try:
        exit_val = pytest.main(pytest_flags)
    except Exception as e:
        print(e)
        exit_val = 1
    sys.exit(exit_val)


def main():
    test, install, override, blender_version = parse_cli()
    if install:
        path = addon_helper.get_addon_path(ADDON)
        if path.exists():
            is_empty = os.listdir(path) == []
            if not(is_empty):
                if override:
                    print(f"Removing addon {ADDON}.")
                    shutil.rmtree(path)
                else:
                    print("Addon already installed and no --override flag was provided.")
        if not path.exists() or is_empty or override:
            print(f"Installing addon {ADDON}.")
            addon_helper.install_addon(ADDON)
        
    if test:
        run_pytest(test_number=test)


if __name__ == '__main__':
    main()
