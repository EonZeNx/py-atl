"""
Action RTPC v01 containers
"""

from py_atl import database
from py_atl.rtpc_v01.containers import RtpcObject, RtpcWorldObject
from py_atl.rtpc_v01 import create
from py_atl.pynet.pyfile import PyFileStream, PyFileMode

from ApexFormat.RTPC.V01.Class import (RtpcV01HeaderExtensions, RtpcV01ContainerExtensions, RtpcV01Container,
                                       IRtpcV01Filter, RtpcV01Filter, RtpcV01FilterString)


def load_from_path(file_path: str) -> RtpcV01Container | None:
    # open file
    with PyFileStream(file_path, PyFileMode.OPEN) as in_buffer:
        option_header = RtpcV01HeaderExtensions.ReadRtpcV01Header(in_buffer.stream)
        if option_header.IsNone:
            return None

        # load file
        option_container = RtpcV01ContainerExtensions.ReadRtpcV01Container(in_buffer.stream)

    if option_container.IsNone:
        return None

    container: RtpcV01Container = option_container.Unwrap()
    return container


def filter_by(container: RtpcV01Container, filters: list[IRtpcV01Filter]) -> RtpcObject | None:
    RtpcV01ContainerExtensions.FilterBy(container, filters)

    # open database for querying shit
    database.setup_jc3()
    rtpc_object: RtpcObject = RtpcObject("root")

    for i in range(len(container.Containers)):
        child_container = container.Containers[i]

        # creating python objects
        world_object: RtpcWorldObject = create.from_rtpc(child_container)

        if world_object is not None:
            rtpc_object.containers.append(world_object)

    return rtpc_object
