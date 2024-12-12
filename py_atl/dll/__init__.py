import pythonnet
if pythonnet.get_runtime_info() is not None:
    pythonnet.unload()

pythonnet.load("coreclr")
import clr

from py_atl import development, addon
from os import path, listdir


def setup_dll(project_path: str, log_result: bool = False):
    if len(project_path) == 0 or not path.exists(project_path):
        return

    dll_directory: str = path.join(project_path, "dll")
    development.DLL_FILES = [path.join(dll_directory, f).removesuffix(".dll")
                             for f in listdir(dll_directory)
                             if path.isfile(path.join(dll_directory, f)) and f.endswith(".dll")]

    loaded_dlls: list[str] = []
    failed_dlls: list[str] = []
    for dll_file in development.DLL_FILES:
        try:
            clr.AddReference(dll_file)
            loaded_dlls.append(dll_file)
        except (Exception,) as e:
            development.log(e)
            failed_dlls.append(dll_file)

    if log_result:
        development.log(f"Successfully loaded {len(loaded_dlls)} dll files")
        for dll in loaded_dlls:
            development.log(f"\t- {dll}")

        development.log(f"Failed to load {len(failed_dlls)}")
        for dll in failed_dlls:
            development.log(f"\t- {dll}")


setup_dll(addon.project_path())
