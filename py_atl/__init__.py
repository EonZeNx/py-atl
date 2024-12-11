bl_info = {
    "name": "PyAtl",
    "blender": (4, 3, 0),
    "category": "Import-Export",
    "description": "Interfaces with ATL",
    "author": "EonZeNx",
    "version": (0, 1, 0),
}

from py_atl import utils, dll
import bpy
from bpy.props import StringProperty
from bpy.types import AddonPreferences


class PyAtlPreferences(AddonPreferences):
    bl_idname = __name__

    project_path: StringProperty(
        name="Project Base Path",
        description="Base path for dll files, database files, and more",
        default="",
        subtype='DIR_PATH',
        update=lambda self, context: self.on_preference_update(context)
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "project_path")

    def on_preference_update(self, context):
        dll.setup_dll(self.project_path)


def register():
    bpy.utils.register_class(PyAtlPreferences)

    from py_atl import utils, dll
    dll.setup_dll(utils.project_path(), True)


def unregister():
    bpy.utils.unregister_class(PyAtlPreferences)


if __name__ == "__main__":
    register()
