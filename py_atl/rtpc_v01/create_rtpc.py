"""

"""

from py_atl import database, development
from py_atl.dll import cs_to
from py_atl.rtpc_v01.containers import RtpcWorldObject, RtpcRigidObject

# these may produce expected warnings
from ApexFormat.RTPC.V01.Class import (RtpcV01Container, RtpcV01Variant, RtpcV01VariantExtensions,
                                       RtpcV01VariantHeaderExtensions)
from ApexToolsLauncher.Core.Hash import JenkinsL3


def get_property(container: RtpcV01Container, property_id: str | int) -> RtpcV01Variant | None:
    property_hash: int = 0
    if type(property_id) is int:
        property_hash = property_id
    elif type(property_id) is str:
        property_hash = JenkinsL3.Jenkins(property_id)
    else:
        raise ValueError(f"RtpcObject initialised with invalid type, {type(property_id)}")

    for container_property in container.Properties:
        if container_property.NameHash == property_hash:
            return container_property

    return None


def create_rtpc_rigid_object(container: RtpcV01Container) -> RtpcRigidObject | None:
    name_property = get_property(container, "name")
    if name_property is None:
        development.log(f"container did not have name property")
        return None

    world_property = get_property(container, "world")
    if world_property is None:
        development.log(f"container did not have world property")
        return None

    filename_hash_property = get_property(container, "filename")
    if filename_hash_property is None:
        development.log(f"container did not have filename property")
        return None

    filename_hash_value: int = RtpcV01VariantHeaderExtensions.AsInt(filename_hash_property)

    option_filename_result = database.lookup_filepath(filename_hash_value)
    if option_filename_result.IsNone:
        development.log(f"failed to find option filename")
        return None

    name_value: str = RtpcV01VariantExtensions.AsString(name_property)
    world_value = cs_to.bpy_matrix(RtpcV01VariantExtensions.AsMat4X4(world_property))
    filename: str = option_filename_result.Unwrap().Value

    rigid_object: RtpcRigidObject = RtpcRigidObject(name_value)
    rigid_object.world = world_value
    rigid_object.filename = filename

    return rigid_object


def create_rtpc_object(container: RtpcV01Container, recurse: bool = True) -> RtpcWorldObject | None:
    class_property = get_property(container, "_class")
    if class_property is None:
        return None

    class_value: str = RtpcV01VariantExtensions.AsString(class_property)

    rtpc_object: RtpcWorldObject | None = None
    if class_value == "CRigidObject":
        rtpc_object = create_rtpc_rigid_object(container)

    if recurse:
        for child_container in container.Containers:
            child_object = create_rtpc_object(child_container, recurse)
            if child_object is not None:
                rtpc_object.containers.append(child_object)

    return rtpc_object
