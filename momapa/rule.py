from typing import Optional, Self

from .os import map_to_generic_arch, map_to_generic_os


# @TODO to validate:
# os: name, version (regex), arch
# features: is_demo_user, has_custom_resolution
class Rule:
    action: str = None
    features: Optional[dict] = None
    os: Optional[dict] = None

    def __init__(self, action: str, features: Optional[dict] = None, os: Optional[dict] = None):
        self.action = action
        self.features = features
        self.os = os

    @staticmethod
    def parse(data: Optional[dict]) -> Optional[Self]:
        if not data:
            return None

        os = data.get('os')
        if os:
            name = os.get('name')
            if name:
                os['name'] = map_to_generic_os(name)

            arch = os.get('arch')
            if arch:
                os['arch'] = map_to_generic_arch(arch)

        return Rule(
            data.get('action'),
            data.get('features'),
            os,
        )
