from System.IO import FileStream, FileMode
from System import Array, String
from System.Collections.Generic import Dictionary
from ApexFormat.RTPC.V01.Class import RtpcV01HeaderExtensions, RtpcV01ContainerExtensions, RtpcV01Container, IRtpcV01Filter, RtpcV01Filter, RtpcV01FilterString


def filter_by(filters: list[IRtpcV01Filter]):
    for each in filters:
        print(each)


def filter_by_test():
    rigid_object: RtpcV01FilterString = RtpcV01FilterString("_class", "CRigidObject")
    rigid_object.SubFilters = [
        RtpcV01Filter("filename"),
        RtpcV01Filter("world")
    ]

    filter_by([rigid_object])
