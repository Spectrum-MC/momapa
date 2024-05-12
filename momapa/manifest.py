from datetime import datetime
from typing import List, Optional, Self

from .logging import Logging
from .file import File
from .asset import AssetIndex
from .argument import GameArgumentSet
from .java import JavaVersion
from .library import GameLibrary


def _parse_datetime(isoformat: Optional[str]) -> Optional[datetime]:
    if not isoformat:
        return None

    return datetime.fromisoformat(isoformat)


class GameDownloads:
    client: File = None
    server: Optional[File] = None
    client_mappings: Optional[File] = None
    server_mappings: Optional[File] = None
    windows_server: Optional[File] = None  # Only in some versions (e.g. 1.6)

    @staticmethod
    def parse(downloads: dict) -> Optional[Self]:
        if not downloads:
            return None

        gd = GameDownloads()

        gd.client = File.parse(downloads.get('client'))
        gd.client_mappings = File.parse(downloads.get('client_mappings'))
        gd.server = File.parse(downloads.get('server'))
        gd.server_mappings = File.parse(downloads.get('server_mappings'))
        gd.windows_server = File.parse(downloads.get('windows_server'))

        return gd


class MojangManifest:
    id: str = None
    type: str = None
    time: datetime = None
    release_time: datetime = None

    jar_files: GameDownloads = None
    assets: AssetIndex = None
    arguments: GameArgumentSet = None
    java_version: JavaVersion = None
    libraries: List[GameLibrary]

    main_class: str = None
    minimum_launcher_version: int = None
    compliance_level: int = None

    logging: Logging = None

    def __init__(self):
        self.libraries = []

    @staticmethod
    def parse(data: dict) -> Optional[Self]:
        if not data:
            return None

        manifest = MojangManifest()

        #region Parsing standard manifest attributes
        manifest.id = data.get('id')
        manifest.type = data.get('type')
        manifest.time = _parse_datetime(data.get('time'))
        manifest.release_time = _parse_datetime(data.get('releaseTime'))
        manifest.main_class = data.get('mainClass')
        manifest.minimum_launcher_version = data.get('minimumLauncherVersion')
        manifest.compliance_level = data.get('complianceLevel')
        #endregion

        manifest.java_version = JavaVersion.parse(data.get('javaVersion'))
        manifest.jar_files = GameDownloads.parse(data.get('downloads'))
        manifest.assets = AssetIndex.parse(data.get('assetIndex'))
        manifest.logging = Logging.parse(data.get('logging'))

        if 'arguments' in data:
            manifest.arguments = GameArgumentSet.parse(data.get('arguments'))
        elif 'minecraftArguments' in data:
            manifest.arguments = GameArgumentSet.parse_legacy(data.get('minecraftArguments'))

        # One library on the Mojang manifest can result
        # in multiple libraries object
        # This is because we want to standardize things
        # no matter the type of manifest we get
        for lib in data.get('libraries', []):
            parsed = GameLibrary.parse(lib)

            if isinstance(parsed, GameLibrary):
                manifest.libraries.append(parsed)
            else:
                for parsed_lib in parsed:
                    manifest.libraries.append(parsed_lib)

        return manifest
