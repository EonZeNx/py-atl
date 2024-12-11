"""
This file expects pythonnet to already have loaded all relevant dll
"""

from py_atl import database, development
from py_atl.dll import cs_to
from py_atl.rtpc_v01.containers import RtpcObject, RtpcWorldObject, RtpcRigidObject

# these may produce expected warnings
from System.IO import FileStream, FileMode
from ApexFormat.RTPC.V01.Class import (RtpcV01HeaderExtensions, RtpcV01ContainerExtensions, RtpcV01Container,
                                       RtpcV01Variant, IRtpcV01Filter, RtpcV01Filter, RtpcV01FilterString,
                                       RtpcV01VariantExtensions, RtpcV01VariantHeaderExtensions)
from ApexToolsLauncher.Core.Hash import JenkinsL3


FILE_PATH: str = r"D:\Games\Avalanche\_Projects\py-atl\test\dlc3_satellite_base_01.blo"
DB_PATH: str = r"D:\Games\Avalanche\_Projects\py-atl\py_atl\database\atl.jc3.db"


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


def main() -> None:
    global FILE_PATH, DB_PATH

    in_buffer = FileStream(FILE_PATH, FileMode.Open)

    option_header = RtpcV01HeaderExtensions.ReadRtpcV01Header(in_buffer)
    if option_header.IsNone:
        return

    option_container = RtpcV01ContainerExtensions.ReadRtpcV01Container(in_buffer)
    if option_container.IsNone:
        return

    container: RtpcV01Container = option_container.Unwrap()

    rigid_object: RtpcV01FilterString = RtpcV01FilterString("_class", "CRigidObject")
    rigid_object.SubFilters = [
        RtpcV01Filter("name"),
        RtpcV01Filter("filename"),
        RtpcV01Filter("world")
    ]

    effect_point_emitter: RtpcV01FilterString = RtpcV01FilterString("_class", "CEffectPointEmitter")
    effect_point_emitter.SubFilters = [
        RtpcV01Filter("name"),
        RtpcV01Filter("effect"),
        RtpcV01Filter("world")
    ]

    dynamic_light_object: RtpcV01FilterString = RtpcV01FilterString("_class", "CDynamicLightObject")
    dynamic_light_object.SubFilters = [
        RtpcV01Filter("name"),
        RtpcV01Filter("diffuse"),
        RtpcV01Filter("falloff_start"),
        RtpcV01Filter("is_spot_light"),
        RtpcV01Filter("multiplier"),
        RtpcV01Filter("on_during_daytime"),
        RtpcV01Filter("projected_texture"),
        RtpcV01Filter("projected_texture_enabled"),
        RtpcV01Filter("projected_texture_u_scale"),
        RtpcV01Filter("projected_texture_v_scale"),
        RtpcV01Filter("radius"),
        RtpcV01Filter("spot_angle"),
        RtpcV01Filter("spot_inner_angle"),
        RtpcV01Filter("volume_intensity"),
        RtpcV01Filter("volumetric_mode"),
        RtpcV01Filter("world"),
    ]

    static_decal_object: RtpcV01FilterString = RtpcV01FilterString("_class", "CStaticDecalObject")
    static_decal_object.SubFilters = [
        RtpcV01Filter("name"),
        RtpcV01Filter("Emissive"),
        RtpcV01Filter("alpha_max"),
        RtpcV01Filter("alpha_min"),
        RtpcV01Filter("alphamask_offset_u"),
        RtpcV01Filter("alphamask_offset_v"),
        RtpcV01Filter("alphamask_source_channel"),
        RtpcV01Filter("alphamask_strength"),
        RtpcV01Filter("alphamask_texture"),
        RtpcV01Filter("alphamask_tile_u"),
        RtpcV01Filter("alphamask_tile_v"),
        RtpcV01Filter("color"),
        RtpcV01Filter("diffuse_texture"),
        RtpcV01Filter("distance_field_decal_mpm"),
        RtpcV01Filter("is_distance_field_stencil"),
        RtpcV01Filter("offset_u"),
        RtpcV01Filter("offset_v"),
        RtpcV01Filter("tile_u"),
        RtpcV01Filter("tile_v"),
        RtpcV01Filter("world"),
    ]

    filters: list[IRtpcV01Filter] = [
        rigid_object,
    ]

    total_before: int = RtpcV01ContainerExtensions.CountContainers(container)
    RtpcV01ContainerExtensions.FilterBy(container, filters)
    total_after: int = RtpcV01ContainerExtensions.CountContainers(container)

    development.log(f"total pre-filter: {total_before}, total post-filter: {total_after}")

    database.setup(DB_PATH)
    py_container = RtpcObject("root")

    for i in range(len(container.Containers)):
        child_container = container.Containers[i]

        world_object: RtpcWorldObject = create_rtpc_object(child_container)
        if world_object is not None:
            py_container.containers.append(world_object)

        if i >= 10:
            break

    development.log(f"{py_container}")


if __name__ == '__main__':
    import pythonnet
    pythonnet.load("coreclr")

    main()
