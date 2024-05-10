from typing import List

from .os import map_to_generic_arch, map_to_generic_os
from .file import PathFile
from .rule import Rule


# Natives for legacy versions are splited in multiple GameLibrary
# Those are differentiated by rules + extract_natives = true
class GameLibrary:
    name: str = None
    rules: List[Rule]
    artifact: PathFile = None

    is_natives: bool = False
    extract_natives: bool = False

    def __init__(self):
        self.rules = []

    @staticmethod
    def parse_current(data: dict) -> list:
        name = data.get('name').split(':')
        native_type = name.pop()

        gl = GameLibrary()
        gl.name = ':'.join(name)  # We remove the native thing for the lib
        gl.artifact = PathFile.parse(data.get('downloads', {}).get('artifact'))
        gl.is_natives = True
        gl.extract_natives = False

        # Using a small python script we print all libraries that have a name with 4 ':'
        # Then `python test.py > natives.txt`
        # then `cat natives.txt | cut -d':' -f4 | sort -n | uniq`
        # native type can be either

        # linux-aarch_64
        # linux-x86_64
        # natives-linux
        # natives-macos
        # natives-macos-arm64
        # natives-windows
        # natives-windows-arm64
        # natives-windows-x86

        native_type_arr = native_type.split('-')
        if native_type.startswith('natives-'):
            native_type_arr.pop(0)

        if len(native_type_arr) == 1:
            native_type_arr.append('x86_64')

        # For now we just override the rule
        # We'll see later if we need to do better stuff
        gl.rules = [
            Rule('allow', os={
                'name': map_to_generic_os(native_type_arr[0]),
                'arch': map_to_generic_arch(native_type_arr[1]),
            })
        ]

        return [gl]

    @staticmethod
    def parse_legacy(data: dict) -> list:
        libs = []
        artifact = data.get('downloads', {}).get('artifact')

        if artifact:
            lib = GameLibrary()
            lib.name = data.get('name')
            lib.artifact = PathFile.parse(artifact)
            lib.is_natives = False
            lib.extract_natives = False

            for r in data.get('rules', []):
                lib.rules.append(Rule.parse(r))

            libs.append(lib)

        natives = data.get('natives', {})
        if natives:
            for k, v in natives.items():
                # This will be a pain to flatten
                # We need to append a rule to use it only on the given OS/Arch
                # BUT we need to skip if there is already a rule for an OS and
                # it doesn't match
                # because Mojang still give all type of natives even though there
                # is a rule to ignore them
                pass

        return libs

    @staticmethod
    def parse(data: dict):
        if not data:
            return None

        name = data.get('name')
        if not name:
            raise Exception('Failed to parse library')

        libs = []
        name = name.split(':')
        if len(name) == 4:
            libs = GameLibrary.parse_current(data)
        elif len(name) == 3:
            libs = GameLibrary.parse_legacy(data)

        if len(libs) == 0:
            return None

        if len(libs) == 1:
            return libs[0]

        return libs
