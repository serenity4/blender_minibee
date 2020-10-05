import argparse
import os
import sys
import shutil
import subprocess
import zipfile
import tarfile
import requests
import re
from glob import glob
from bs4 import BeautifulSoup


def get_suffix(blender_version):
    if "win32" == sys.platform or "win64" == sys.platform:
        machine = "windows64"
        print(f"Platform: {machine}")
        ext = "zip"
    elif "darwin" == sys.platform:
        machine = "macOS"
        ext = "dmg"
    else:
        machine = "linux.*64"
        ext = "tar.+"

    g = re.search(f"\d\.\d\d", blender_version)
    if g:
        version = g.group(0)
    else:
        raise ValueError("Invalid version format. Expected 'X.XX' such as 2.82.")

    urls = [
        f"https://ftp.nluug.nl/pub/graphics/blender/release/Blender{version}",
        "https://builder.blender.org/download",
    ]
    blender_zippath = None
    nightly = False
    for url in urls:
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")

        blender_version_suffix = ""
        versions_found = []
        for link in soup.find_all("a"):
            x = str(link.get("href"))
            # print(x)
            g = re.search(f"blender-(.+)-{machine}.+{ext}", x)
            if g:
                version_found = g.group(1).split("-")[0]
                versions_found.append(version_found)
                if version_found == blender_version:
                    blender_zippath = f"{url}/{g.group(0)}"
                    if url == urls[1]:
                        nightly = True

    if not blender_zippath:
        print(soup)
        raise Exception(f"Unable to find {blender_version} in nightlies, here is what is available {versions_found}.")

    return blender_zippath, nightly


def get_python_executable(zfiles):
    for zfile in zfiles:
        if re.search(f"bin/python.exe", zfile) or re.search(f"bin/python\d.\d", zfile):
            python = os.path.realpath(zfile)
    return os.path.realpath(python)


def get_archive_references(blender_zipfile):
    # get archive reference
    if blender_zipfile.endswith("zip"):
        z = zipfile.ZipFile(blender_zipfile, "r")
        zfiles = z.namelist()
    elif blender_zipfile.endswith("dmg"):
        raise Exception(f"dmg Unsupported")
        # hdiutil attach -mountpoint <path-to-desired-mountpoint> <filename.dmg>
    else:
        z = tarfile.open(blender_zipfile)
        zfiles = z.getnames()
    zdir = zfiles[0].split("/")[0]
    return z, zdir, zfiles


def uncompress_archive(blender_zipfile):
    z, archive, files = get_archive_references(blender_zipfile)
    # uncompress
    if not os.path.isdir(archive):
        print(f"Unpacking {blender_zipfile}.")
        z.extractall()
    z.close()
    return archive, files


def enter_cache_dir():
    # setup target directory
    if "BLENDER_CACHE" in os.environ.keys():  # Travis CI uses this env variable
        print(f"BLENDER_CACHE found {os.environ['BLENDER_CACHE']}.")
        os.chdir(os.environ["BLENDER_CACHE"])
    else:
        os.chdir("external")


def download_blender(blender_zipfile, blender_zippath):
    # download blender if not already downloaded
    files = glob(blender_zipfile)
    if len(files) == 0:
        if not os.path.exists(blender_zipfile):
            r = requests.get(blender_zippath, stream=True)
            print(f"Downloading {blender_zippath}.")
            with open(blender_zipfile, "wb") as ofile:
                ofile.write(r.content)


def install_python_dependencies(python):
    cwd = os.getcwd()
    print("Installing pip.")
    os.system(f"{python} -m ensurepip")
    os.system(f"{python} -m pip install -U pip")
    print("Installing Python dependencies.")
    os.system(f"{python} -m pip install --upgrade -r {cwd}{os.sep}requirements_blender.txt -r {cwd}{os.sep}requirements.txt")


def move_blender_archive_to_dest(cache_dir, dst, archive):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    src = os.path.join(cache_dir, archive)
    print(f"Moving {src} to {dst}.")
    shutil.move(src, dst)


def create_config(archive, blender_version):
    config_path = os.path.join(archive, blender_version, "config")
    os.makedirs(config_path)


def get_blender(blender_version, blender_zippath, nightly):
    cwd = os.getcwd()
    external_dir = "external"  # target directory
    os.makedirs(external_dir, exist_ok=True)
    enter_cache_dir()
    cache_dir = os.getcwd()

    blender_zipfile = blender_zippath.split("/")[-1]
    download_blender(blender_zipfile, blender_zippath)
    archive, files = uncompress_archive(blender_zipfile)
    create_config(archive, blender_version)

    os.remove(blender_zipfile)

    python = get_python_executable(files)
    os.chdir(cwd)
    install_python_dependencies(python)

    shutil.rmtree(os.path.join("tests", "__pycache__"), ignore_errors=True)

    ext = ""
    if nightly == True:
        ext = "-nightly"
    dst = f"{external_dir}{os.sep}blender-{blender_version}{ext}"

    move_blender_archive_to_dest(cache_dir, dst, archive)


def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bversion', type=str, default='2.82', help="Blender version to fetch.")
    args = parser.parse_args()
    return args.bversion


def main():
    blender_version = parse_cli()
    try:
        build_dir = os.environ["TRAVIS_BUILD_DIR"]
        os.chdir(build_dir)
    except KeyError:
        pass

    if "-" in blender_version:
        blender_version = blender_version.split("-")[0]
    blender_zipfile, nightly = get_suffix(blender_version)
    get_blender(blender_version, blender_zipfile, nightly)


if __name__ == "__main__":
    main()
