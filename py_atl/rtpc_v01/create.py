"""

"""
import mathutils

from py_atl import database, development
from py_atl.dll import cs_to
from py_atl.rtpc_v01.containers import RtpcWorldObject, RtpcRigidObject, RtpcStaticDecalObject, RtpcDynamicLightObject

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


def get_properties(container: RtpcV01Container, property_names: list[str]) -> (dict[str, RtpcV01Variant], list[str]):
    property_hashes: dict[int, str] = {JenkinsL3.Jenkins(name): name for name in property_names}

    properties: dict[str, RtpcV01Variant] = {}
    for container_property in container.Properties:
        if container_property.NameHash not in property_hashes:
            continue

        name: str = property_hashes[container_property.NameHash]
        properties[name] = container_property

    not_found: list[str] = [name for name in property_names if name not in properties]
    return properties, not_found


def to_rigid_object(container: RtpcV01Container) -> RtpcRigidObject | None:
    properties, not_found = get_properties(container, [
        "name",
        "world",
        "filename",
    ])

    if len(not_found) > 0:
        development.log(f"container did not have {len(not_found)} property/ies")
        print(not_found)
        return None

    name_property = properties.get("name")
    world_property = properties.get("world")
    filename_hash_property = properties.get("filename")

    filename_hash_value: int = RtpcV01VariantHeaderExtensions.AsInt(filename_hash_property)
    option_filename_result = database.lookup_filepath(filename_hash_value)
    if option_filename_result.IsNone:
        development.log(f"failed to find filename '{filename_hash_value}'")
        return None

    name_value: str = RtpcV01VariantExtensions.AsString(name_property)
    world_value = cs_to.bpy_matrix(RtpcV01VariantExtensions.AsFloatArray(world_property))
    filename: str = option_filename_result.Unwrap().Value

    rigid_object: RtpcRigidObject = RtpcRigidObject(name_value)
    rigid_object.world = world_value
    rigid_object.filename = filename

    return rigid_object


def to_static_decal(container: RtpcV01Container) -> RtpcStaticDecalObject | None:
    properties, not_found = get_properties(container, [
        "name",
        "Emissive",
        "alpha_max",
        "alpha_min",
        "alphamask_offset_u",
        "alphamask_offset_v",
        "alphamask_source_channel",
        "alphamask_texture",
        "alphamask_tile_u",
        "alphamask_tile_v",
        "color",
        "diffuse_texture",
        "is_distance_field_stencil",
        "offset_u",
        "offset_v",
        "tile_u",
        "tile_v",
        "world",
    ])

    if len(not_found) > 0:
        development.log(f"container did not have {len(not_found)} property/ies")
        print(not_found)
        return None

    name_property = properties.get("name")
    emissive_property = properties.get("Emissive")
    alpha_max_property = properties.get("alpha_max")
    alpha_min_property = properties.get("alpha_min")
    alphamask_offset_u_property = properties.get("alphamask_offset_u")
    alphamask_offset_v_property = properties.get("alphamask_offset_v")
    alphamask_source_channel_property = properties.get("alphamask_source_channel")
    alphamask_texture_property = properties.get("alphamask_texture")
    alphamask_tile_u_property = properties.get("alphamask_tile_u")
    alphamask_tile_v_property = properties.get("alphamask_tile_v")
    color_property = properties.get("color")
    diffuse_texture_property = properties.get("diffuse_texture")
    is_distance_field_stencil_property = properties.get("is_distance_field_stencil")
    offset_u_property = properties.get("offset_u")
    offset_v_property = properties.get("offset_v")
    tile_u_property = properties.get("tile_u")
    tile_v_property = properties.get("tile_v")
    world_property = properties.get("world")

    name_value: str = RtpcV01VariantExtensions.AsString(name_property)
    emissive_value: float = RtpcV01VariantHeaderExtensions.AsFloat(emissive_property)
    alpha_max_value: float = RtpcV01VariantHeaderExtensions.AsFloat(alpha_max_property)
    alpha_min_value: float = RtpcV01VariantHeaderExtensions.AsFloat(alpha_min_property)
    alphamask_offset_u_value: float = RtpcV01VariantHeaderExtensions.AsFloat(alphamask_offset_u_property)
    alphamask_offset_v_value: float = RtpcV01VariantHeaderExtensions.AsFloat(alphamask_offset_v_property)
    alphamask_source_channel_value: int = RtpcV01VariantHeaderExtensions.AsInt(alphamask_source_channel_property)
    alphamask_texture_value: str = RtpcV01VariantExtensions.AsString(alphamask_texture_property)
    alphamask_tile_u_value: float = RtpcV01VariantHeaderExtensions.AsFloat(alphamask_tile_u_property)
    alphamask_tile_v_value: float = RtpcV01VariantHeaderExtensions.AsFloat(alphamask_tile_v_property)
    color_value: mathutils.Euler = cs_to.bpy_euler(RtpcV01VariantExtensions.AsFloatArray(color_property))
    diffuse_texture_value: str = RtpcV01VariantExtensions.AsString(diffuse_texture_property)
    is_distance_field_stencil_value: bool = RtpcV01VariantHeaderExtensions.AsInt(is_distance_field_stencil_property) == 1
    offset_u_value: float = RtpcV01VariantHeaderExtensions.AsFloat(offset_u_property)
    offset_v_value: float = RtpcV01VariantHeaderExtensions.AsFloat(offset_v_property)
    tile_u_value: float = RtpcV01VariantHeaderExtensions.AsFloat(tile_u_property)
    tile_v_value: float = RtpcV01VariantHeaderExtensions.AsFloat(tile_v_property)
    world_value = cs_to.bpy_matrix(RtpcV01VariantExtensions.AsFloatArray(world_property))

    decal: RtpcStaticDecalObject = RtpcStaticDecalObject(name_value)
    decal.Emissive = emissive_value
    decal.alpha_max = alpha_max_value
    decal.alpha_min = alpha_min_value
    decal.alphamask_offset_u = alphamask_offset_u_value
    decal.alphamask_offset_v = alphamask_offset_v_value
    decal.alphamask_source_channel = alphamask_source_channel_value
    decal.alphamask_texture = alphamask_texture_value
    decal.alphamask_tile_u = alphamask_tile_u_value
    decal.alphamask_tile_v = alphamask_tile_v_value
    decal.color = color_value
    decal.diffuse_texture = diffuse_texture_value
    decal.is_distance_field_stencil = is_distance_field_stencil_value
    decal.offset_u = offset_u_value
    decal.offset_v = offset_v_value
    decal.tile_u = tile_u_value
    decal.tile_v = tile_v_value
    decal.world = world_value

    return decal

def to_dynamic_light(container: RtpcV01Container) -> RtpcDynamicLightObject | None:
    properties, not_found = get_properties(container, [
        "name",
        "diffuse",
        "is_spot_light",
        "multiplier",
        "on_during_daytime",
        "projected_texture",
        "projected_texture_enabled",
        "projected_texture_u_scale",
        "projected_texture_v_scale",
        "radius",
        "spot_angle",
        "spot_inner_angle",
        "world",
    ])

    if len(not_found) > 0:
        development.log(f"container did not have {len(not_found)} property/ies")
        print(not_found)
        return None

    name_property = properties.get("name")
    diffuse_property = properties.get("diffuse")
    is_spot_light_property = properties.get("is_spot_light")
    multiplier_property = properties.get("multiplier")
    on_during_daytime_property = properties.get("on_during_daytime")
    projected_texture_property = properties.get("projected_texture")
    projected_texture_enabled_property = properties.get("projected_texture_enabled")
    projected_texture_u_scale_property = properties.get("projected_texture_u_scale")
    projected_texture_v_scale_property = properties.get("projected_texture_v_scale")
    radius_property = properties.get("radius")
    spot_angle_property = properties.get("spot_angle")
    spot_inner_angle_property = properties.get("spot_inner_angle")
    world_property = properties.get("world")

    name_value: str = RtpcV01VariantExtensions.AsString(name_property)
    diffuse_value: mathutils.Euler = cs_to.bpy_euler(RtpcV01VariantExtensions.AsFloatArray(diffuse_property))
    is_spot_light_value: int = RtpcV01VariantHeaderExtensions.AsInt(is_spot_light_property)
    multiplier_value: float = RtpcV01VariantHeaderExtensions.AsFloat(multiplier_property)
    on_during_daytime_value: int = RtpcV01VariantHeaderExtensions.AsInt(on_during_daytime_property)
    projected_texture_value: int = RtpcV01VariantHeaderExtensions.AsInt(projected_texture_property)
    projected_texture_enabled_value: int = RtpcV01VariantHeaderExtensions.AsInt(projected_texture_enabled_property)
    projected_texture_u_scale_value: float = RtpcV01VariantHeaderExtensions.AsFloat(projected_texture_u_scale_property)
    projected_texture_v_scale_value: float = RtpcV01VariantHeaderExtensions.AsFloat(projected_texture_v_scale_property)
    radius_value: float = RtpcV01VariantHeaderExtensions.AsFloat(radius_property)
    spot_angle_value: float = RtpcV01VariantHeaderExtensions.AsFloat(spot_angle_property)
    spot_inner_angle_value: float = RtpcV01VariantHeaderExtensions.AsFloat(spot_inner_angle_property)
    world_value = cs_to.bpy_matrix(RtpcV01VariantExtensions.AsFloatArray(world_property))

    light: RtpcDynamicLightObject = RtpcDynamicLightObject(name_value)
    light.diffuse = diffuse_value
    light.is_spot_light = is_spot_light_value
    light.multiplier = multiplier_value
    light.on_during_daytime = on_during_daytime_value
    light.projected_texture = projected_texture_value
    light.projected_texture_enabled = projected_texture_enabled_value
    light.projected_texture_u_scale = projected_texture_u_scale_value
    light.projected_texture_v_scale = projected_texture_v_scale_value
    light.radius = radius_value
    light.spot_angle = spot_angle_value
    light.spot_inner_angle = spot_inner_angle_value
    light.world = world_value

    return light

def from_rtpc(container: RtpcV01Container, recurse: bool = True) -> RtpcWorldObject | None:
    class_property = get_property(container, "_class")
    if class_property is None:
        return None

    class_value: str = RtpcV01VariantExtensions.AsString(class_property)

    rtpc_object: RtpcWorldObject | None = None
    if class_value == "CRigidObject":
        rtpc_object = to_rigid_object(container)
    elif class_value == "CStaticDecalObject":
        rtpc_object = to_static_decal(container)
    elif class_value == "CDynamicLightObject":
        rtpc_object = to_dynamic_light(container)

    if recurse:
        for child_container in container.Containers:
            child_object = from_rtpc(child_container, recurse)
            if child_object is not None:
                rtpc_object.containers.append(child_object)

    return rtpc_object
