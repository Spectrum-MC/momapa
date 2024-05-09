from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class JarFile:
    url: str
    size: int
    hash: str


class Rule:
    action: str
    features: Optional[dict]
    os: Optional[dict]

    def __init__(self, action: str, features: Optional[dict] = None, os: Optional[dict] = None):
        self.action = action
        self.features = features
        self.os = os

@dataclass
class Argument:
    values: List[str]
    rules: List[Rule]


@dataclass
class GameArgumentSet:
    game: List[Argument]
    jvm: List[Argument]


class AssetIndex:
    id: str
    hash: str
    size: int
    total_size: int
    url: str


class GameDownloads:
    client: JarFile
    server: Optional[JarFile]
    client_mappings: Optional[JarFile]
    server_mappings: Optional[JarFile]


class JavaVersion:
    component: str
    major_version: int


class MojangManifest:
    id: str
    type: str
    time: datetime
    release_time: datetime

    jar_files: GameDownloads
    assets: AssetIndex
    arguments: GameArgumentSet
    java_version: JavaVersion

    main_class: str
    minimum_launcher_version: int
    compliance_level: int