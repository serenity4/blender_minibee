import os
import bpy
import sys
import typing
import inspect
import pkgutil
import importlib
from itertools import chain
from pathlib import Path
from pprint import pprint
from .log import logger

__all__ = (
    "init",
    "register",
    "unregister",
)

modules = None
ordered_classes = None

def init_modules():
    global modules
    modules = get_all_submodules()

def init_classes():
    global ordered_classes
    ordered_classes = get_ordered_classes_to_register(modules)


def register():
    if ordered_classes:
        logger.debug(f"\033[32;1;1m--- Registering classes\033[m")
    for cls in ordered_classes:
        logger.debug(f"    \033[33;1;1m--> {cls.__name__}\033[m")
        bpy.utils.register_class(cls)


    logger.debug("\033[32;1;1m--- Registering modules\033[m")
    for module in modules:
        if module.__name__ == __name__:
            continue
        if hasattr(module, "register"):
            logger.debug(f"    \033[33;1;1m--> {module.__name__}\033[m")
            module.register()
    print("\n" * 5)


def unregister():
    if ordered_classes:
        logger.debug(f"--- Unregistering classes")
    for cls in reversed(ordered_classes):
        logger.debug(f"    --> {cls.__name__}")
        bpy.utils.unregister_class(cls)
    logger.debug("--- Unregistering modules")

    for module in modules:
        if module.__name__ == __name__:
            continue
        if hasattr(module, "unregister"):
            logger.debug(f"    --> {cls.__name__}")
            module.unregister()


# Import modules
#################################################

def get_all_submodules():
    return list(_find_all_importables(sys.modules[__package__]))

def _find_all_importables(pkg):
    """Find all importables in the project.
    Return them in order.
    """
    return set(chain.from_iterable(_discover_path_importables(Path(p), pkg.__name__) for p in pkg.__path__))


def _discover_path_importables(pkg_pth, pkg_name):
    """Yield all importables under a given path and package."""
    for dir_path, _d, file_names in os.walk(pkg_pth):
        pkg_dir_path = Path(dir_path)

        if pkg_dir_path.parts[-1] == '__pycache__':
            continue

        if all(Path(_).suffix != '.py' for _ in file_names):
            continue

        rel_pt = pkg_dir_path.relative_to(pkg_pth)
        pkg_pref = '.'.join((pkg_name, ) + rel_pt.parts)
        yield from (
            importlib.import_module(pkg_path)
            for _, pkg_path, _ in pkgutil.walk_packages(
                (str(pkg_dir_path), ), prefix=f'{pkg_pref}.',
            )
        )


# Find classes to register
#################################################

def get_ordered_classes_to_register(modules):
    return toposort(get_register_deps_dict(modules))


def get_register_deps_dict(modules):
    deps_dict = {}
    classes_to_register = set(iter_classes_to_register(modules))
    for cls in classes_to_register:
        deps_dict[cls] = set(iter_own_register_deps(cls, classes_to_register))
    return deps_dict


def iter_own_register_deps(cls, own_classes):
    yield from (dep for dep in iter_register_deps(cls) if dep in own_classes)


def iter_register_deps(cls):
    for value in typing.get_type_hints(cls, {}, {}).values():
        dependency = get_dependency_from_annotation(value)
        if dependency is not None:
            yield dependency


def get_dependency_from_annotation(value):
    if isinstance(value, tuple) and len(value) == 2:
        if value[0] in (bpy.props.PointerProperty, bpy.props.CollectionProperty):
            return value[1]["type"]
    return None


def iter_classes_to_register(modules):
    base_types = get_register_base_types()
    for cls in get_classes_in_modules(modules):
        if any(base in base_types for base in cls.__bases__):
            if not getattr(cls, "is_registered", False):
                yield cls


def get_classes_in_modules(modules):
    classes = set()
    for module in modules:
        for cls in iter_classes_in_module(module):
            classes.add(cls)
    return classes


def iter_classes_in_module(module):
    for value in module.__dict__.values():
        if inspect.isclass(value):
            yield value


def get_register_base_types():
    return set(getattr(bpy.types, name) for name in [
        "Panel", "Operator", "PropertyGroup",
        "AddonPreferences", "Header", "Menu",
        "Node", "NodeSocket", "NodeTree",
        "UIList", "RenderEngine"
    ])


# Find order to register to solve dependencies
#################################################

def toposort(deps_dict):
    sorted_list = []
    sorted_values = set()
    while len(deps_dict) > 0:
        unsorted = []
        for value, deps in deps_dict.items():
            if len(deps) == 0:
                sorted_list.append(value)
                sorted_values.add(value)
            else:
                unsorted.append(value)
        deps_dict = {value: deps_dict[value] - sorted_values for value in unsorted}
    return sorted_list
