from typing import List

from .os import map_to_generic_arch, map_to_generic_os, RuleAction, OS
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
            Rule(RuleAction.ALLOW, os={
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
                v = data.get('downloads', {}).get('classifiers', {}).get(v)
                k = map_to_generic_os(k)

                lib = GameLibrary()
                lib.name = data.get('name')
                lib.artifact = PathFile.parse(v)
                lib.is_natives = True
                lib.extract_natives = True if data.get('natives') else False

                #region Hack for 1.8-ish versions OSX
                # Those have natives-osx BUT ALSO
                # DISALLOW OSX
                # E.g. https://piston-meta.mojang.com/v1/packages/1fade4fe9d2587106ac3fa14775f9126d3198103/15w35e.json
                # org.lwjgl.lwjgl:lwjgl-platform:2.9.4-nightly-20150209
                should_skip = False
                if k == OS.OSX:
                    for r in data.get('rules', []):
                        if r.get('action') != 'disallow':
                            continue

                        if r.get('os', {}).get('name') == 'osx':
                            should_skip = True

                if should_skip:
                    continue
                #endregion

                lib.rules = [
                    Rule(RuleAction.ALLOW, None, {
                        'name': k,
                    })
                ]

                libs.append(lib)

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
