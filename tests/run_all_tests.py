import argparse
from pathlib import Path
import sys
import os
import re

import subprocess

search_pattern = re.compile(r"test_(\d+)")

def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bversion', type=str, default='2.82', help="Blender version with which to run the tests.")
    parser.add_argument('--override', action='store_true', help='Overrides existing addon, if one has already been installed.')
    args = parser.parse_args()
    return args.bversion, args.override

def main():
    bversion, override = parse_cli()
    test_numbers = list(map(lambda x: re.search(search_pattern, x).group(1), [item for item in os.listdir('tests') if Path(f'tests/{item}').is_dir()]))
    if not test_numbers:
        print(f"No test directories found under {Path(f'{Path.cwd()}/tests')}.")
        sys.exit(1)
    return_codes = []

    for number in test_numbers:
        flags = [f"--bversion={bversion}", "--install", f"--test={number}"]
        if override:
            flags.append("--override")
        p = subprocess.run(["python", "scripts/run_blender.py", *flags])
        return_codes.append(p.returncode)
    
    if any(return_codes):
        failed_indices = [str(index + 1) for index, code in enumerate(return_codes) if code]
        print(f"Test failed for test subdirectories {', '.join(failed_indices)}")
        sys.exit(1)
    else:
        print("All tests successfully passed!")
        sys.exit(0)

if __name__ == '__main__':
    main()