"""

"""

from py_atl import database, development
from py_atl.dll import cs_to
from py_atl.rtpc_v01.containers import RtpcWorldObject, RtpcRigidObject, RtpcStaticDecalObject

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

    rigid_object: RtpcStaticDecalObject = RtpcStaticDecalObject(name_value)
    rigid_object.world = world_value
    rigid_object.filename = filename

    return rigid_object

def to_decal(container: RtpcV01Container) -> RtpcStaticDecalObject | None:
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
    world_property = properties.get("world")
    diffuse_texture_property = properties.get("diffuse_texture")
    alphamask_texture_property = properties.get("alphamask_texture")

    # Resolve diffuse_texture filepath
    diffuse_texture_hash_value: int = RtpcV01VariantHeaderExtensions.AsInt(diffuse_texture_property)
    option_diffuse_texture_result = database.lookup_filepath(diffuse_texture_hash_value)
    if option_diffuse_texture_result.IsNone:
        development.log(f"failed to find diffuse_texture '{diffuse_texture_hash_value}'")
        return None

    # Resolve alphamask_texture filepath
    alphamask_texture_hash_value: int = RtpcV01VariantHeaderExtensions.AsInt(alphamask_texture_property)
    option_alphamask_texture_result = database.lookup_filepath(alphamask_texture_hash_value)
    if option_alphamask_texture_result.IsNone:
        development.log(f"failed to find alphamask_texture '{alphamask_texture_hash_value}'")
        return None

    name_value: str = RtpcV01VariantExtensions.AsString(name_property)
    world_value = cs_to.bpy_matrix(RtpcV01VariantExtensions.AsFloatArray(world_property))
    diffuse_filename: str = option_diffuse_texture_result.Unwrap().Value
    alphamask_filename: str = option_alphamask_texture_result.Unwrap().Value

    decal: RtpcStaticDecalObject = RtpcStaticDecalObject(name_value)
    decal.world = world_value
    decal.diffuse_texture = diffuse_filename
    decal.alphamask_texture = alphamask_filename
    decal.Emissive = RtpcV01VariantExtensions.AsFloat(properties.get("Emissive", 0))
    decal.alpha_max = RtpcV01VariantExtensions.AsFloat(properties.get("alpha_max", 0))
    decal.alpha_min = RtpcV01VariantExtensions.AsFloat(properties.get("alpha_min", 0))
    decal.alphamask_offset_u = RtpcV01VariantExtensions.AsFloat(properties.get("alphamask_offset_u", 0))
    decal.alphamask_offset_v = RtpcV01VariantExtensions.AsFloat(properties.get("alphamask_offset_v", 0))
    decal.alphamask_source_channel = RtpcV01VariantExtensions.AsInt(properties.get("alphamask_source_channel", 0))
    decal.alphamask_tile_u = RtpcV01VariantExtensions.AsFloat(properties.get("alphamask_tile_u", 0))
    decal.alphamask_tile_v = RtpcV01VariantExtensions.AsFloat(properties.get("alphamask_tile_v", 0))
    decal.color = RtpcV01VariantExtensions.AsEuler(properties.get("color", mathutils.Euler((0, 0, 0))))
    decal.is_distance_field_stencil = RtpcV01VariantExtensions.AsInt(properties.get("is_distance_field_stencil", 0))
    decal.offset_u = RtpcV01VariantExtensions.AsFloat(properties.get("offset_u", 0))
    decal.offset_v = RtpcV01VariantExtensions.AsFloat(properties.get("offset_v", 0))
    decal.tile_u = RtpcV01VariantExtensions.AsFloat(properties.get("tile_u", 0))
    decal.tile_v = RtpcV01VariantExtensions.AsFloat(properties.get("tile_v", 0))

    return decal

def from_rtpc(container: RtpcV01Container, recurse: bool = True) -> RtpcWorldObject | None:
    class_property = get_property(container, "_class")
    if class_property is None:
        return None

    class_value: str = RtpcV01VariantExtensions.AsString(class_property)

    rtpc_object: RtpcWorldObject | None = None
    if class_value == "CRigidObject":
        rtpc_object = to_rigid_object(container)
    elif class_value == "CStaticDecalObject":
        rtpc_object = to_decal(container)

    if recurse:
        for child_container in container.Containers:
            child_object = from_rtpc(child_container, recurse)
            if child_object is not None:
                rtpc_object.containers.append(child_object)

    return rtpc_object
