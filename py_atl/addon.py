import bpy


def project_path() -> str:
    addon = bpy.context.preferences.addons.get("py_atl", None)
    if addon is None:
        return ""

    preferences = addon.preferences
    if preferences is None:
        return ""

    project_path = preferences.project_path
    if project_path is None:
        return ""

    return project_path
