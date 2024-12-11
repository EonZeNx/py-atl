from dataclasses import dataclass, field
from typing import Self


@dataclass(slots=True)
class RtpcObject:
    init_value: str | int | None = field(init=True, default=None)
    name: str | None = field(init=False, default=None)
    name_hash: int | None = field(init=False, default=None)
    containers: list[Self] = field(init=False, default_factory=list)

    def __post_init__(self):
        if type(self.init_value) is str:
            self.name = self.init_value
        elif type(self.init_value) is int:
            self.name_hash = self.init_value
        else:
            raise ValueError(f"{type(self).__name__} initialised with invalid type, {type(self.init_value)}")

        if self.name is None and self.name_hash is None:
            raise ValueError(f"{type(self).__name__} must have name or name_hash")

    def __repr__(self):
        name_or_hash: str = self.name if self.name is not None else f"{self.name_hash:08X}"
        containers_str: str = f"containers: {self.containers}" if len(self.containers) > 0 else ""
        containers_prefix: str = ", " if len(containers_str) > 0 else ""

        return f"{type(self).__name__}({name_or_hash}{containers_prefix}{containers_str})"


@dataclass(slots=True)
class RtpcWorldObject(RtpcObject):
    world: str = field(init=False, default=None)

    def __repr__(self):
        name_or_hash: str = self.name if self.name is not None else f"{self.name_hash:08X}"
        containers_str: str = f"containers: {self.containers}" if len(self.containers) > 0 else ""
        containers_prefix: str = ", " if len(containers_str) > 0 else ""

        return f"{type(self).__name__}({name_or_hash}, world: {self.world}{containers_prefix}{containers_str})"


@dataclass(slots=True)
class RtpcRigidObject(RtpcWorldObject):
    filename: str | None = field(init=False, default=None)
    filename_hash: int | None = field(init=False, default=None)

    def __repr__(self):
        name_or_hash: str = self.name if self.name is not None else f"{self.name_hash:08X}"
        containers_str: str = f"containers: {self.containers}" if len(self.containers) > 0 else ""
        containers_prefix: str = ", " if len(containers_str) > 0 else ""
        filename_or_hash: str = self.filename if self.filename is not None else f"{self.filename_hash:08X}"

        return f"{type(self).__name__}({name_or_hash}, filename: {filename_or_hash}, world: {self.world}{containers_prefix}{containers_str})"

