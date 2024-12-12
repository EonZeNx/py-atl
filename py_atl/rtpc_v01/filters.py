"""
Various filters for RTPC v01 containers
"""

# these may produce expected warnings
from ApexFormat.RTPC.V01.Class import (RtpcV01ContainerExtensions, RtpcV01Container, IRtpcV01Filter, RtpcV01Filter,
                                       RtpcV01FilterString)


RIGID_OBJECT: RtpcV01FilterString = RtpcV01FilterString("_class", "CRigidObject", [
    RtpcV01Filter("name"),
    RtpcV01Filter("filename"),
    RtpcV01Filter("world")
])

FX_POINT_EMITTER: RtpcV01FilterString = RtpcV01FilterString("_class", "CEffectPointEmitter", [
    RtpcV01Filter("name"),
    RtpcV01Filter("effect"),
    RtpcV01Filter("world")
])

DYNAMIC_LIGHT_OBJECT: RtpcV01FilterString = RtpcV01FilterString("_class", "CDynamicLightObject", [
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
])

STATIC_DECAL_OBJECT: RtpcV01FilterString = RtpcV01FilterString("_class", "CStaticDecalObject", [
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
])
