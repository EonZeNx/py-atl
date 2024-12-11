"""
This file expects pythonnet to already have loaded all relevant dll
"""

from py_atl import database, development
from py_atl.rtpc_v01.containers import RtpcObject, RtpcWorldObject
from py_atl.rtpc_v01 import create_rtpc

# these may produce expected warnings
from System.IO import FileStream, FileMode
from ApexFormat.RTPC.V01.Class import (RtpcV01HeaderExtensions, RtpcV01ContainerExtensions, RtpcV01Container,
                                       IRtpcV01Filter, RtpcV01Filter, RtpcV01FilterString)


FILE_PATH: str = r"D:\Games\Avalanche\_Projects\py-atl\test\dlc3_satellite_base_01.blo"


def main() -> None:
    global FILE_PATH

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

    database.setup_jc3()
    py_container = RtpcObject("root")

    for i in range(len(container.Containers)):
        child_container = container.Containers[i]

        world_object: RtpcWorldObject = create_rtpc.create_rtpc_object(child_container)
        if world_object is not None:
            py_container.containers.append(world_object)

        if i >= 10:
            break

    development.log(f"{py_container}")


if __name__ == '__main__':
    import pythonnet
    pythonnet.load("coreclr")

    main()
