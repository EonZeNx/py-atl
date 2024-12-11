import os
import pythonnet
from py_atl import database

PROJECT_DIRECTORY: str = r"D:\Projects\Various\pysharp"
DLL_DIRECTORY: str = os.path.join(PROJECT_DIRECTORY, "dll")
DB_PATH: str = os.path.join(PROJECT_DIRECTORY, "database", "atl.jc3.db")


def setup_dll():
    global DLL_DIRECTORY

    from os import listdir
    from os.path import isfile, join

    pythonnet.load("coreclr")

    import clr

    dll_files: list[str] = [f.removesuffix(".dll") for f in listdir(DLL_DIRECTORY) if isfile(join(DLL_DIRECTORY, f)) and f.endswith(".dll")]
    for dll_file in dll_files:
        clr.AddReference(dll_file)

    import pysharp
    pysharp.main()


if __name__ == '__main__':
    setup_dll()
    database.setup(DB_PATH)
