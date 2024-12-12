from py_atl import development
from py_atl.rtpc_v01 import action, filters
from py_atl.rtpc_v01.containers import RtpcObject

# these may produce expected warnings
from ApexFormat.RTPC.V01.Class import (RtpcV01HeaderExtensions, RtpcV01ContainerExtensions, RtpcV01Container,
                                       IRtpcV01Filter, RtpcV01Filter, RtpcV01FilterString)


def filter_example(path: str) -> None:
    container: RtpcV01Container | None = action.load_from_path(path)
    if container is None:
        development.log(f"failed to load container from '{path}'")
        return

    rtpc_object: RtpcObject = action.filter_by(container, [
        filters.RIGID_OBJECT,
        filters.FX_POINT_EMITTER,
        filters.DYNAMIC_LIGHT_OBJECT,
        filters.STATIC_DECAL_OBJECT,
    ])

    development.log(f"{rtpc_object}")


# use it like this:
#
# from py_atl.examples import rtpc_v01
#
# FILE_PATH: str = r"PATH\TO\RTPC.blo"
#
# rtpc_v01.filter_example(FILE_PATH)
