from enum import Enum
from abc import ABC, abstractmethod
import platform


class OS(Enum):
    WINDOWS = 'windows'
    OSX = 'osx'
    LINUX = 'linux'
    UNKNOWN = 'unknown'


class Architecture(Enum):
    I386 = 'i386'
    AMD64 = 'x86_64'
    ARM32 = 'arm'
    ARM64 = 'aarch64'
    UNKNOWN = 'unknown'


class RuleAction(Enum):
    ALLOW = 'allow'
    DISALLOW = 'disallow'
    UNKNOWN = 'unknown'


# @TODO: Do some test to do other
def map_to_generic_arch(arch: str):
    match arch:
        case 'x86_64':
            return Architecture.AMD64

        case 'arm64' | 'aarch_64':
            return Architecture.ARM64

        case 'x86':
            return Architecture.I386

        case _:
            return Architecture.UNKNOWN


def map_to_generic_os(os: str):
    match os:
        case 'Windows' | 'windows':
            return OS.WINDOWS
        case 'Darwin' | 'macos' | 'osx':
            return OS.OSX
        case 'Linux' | 'linux':
            return OS.LINUX
        case _:
            return OS.UNKNOWN


class AbstractArchitectureGetter(ABC):
    @abstractmethod
    def get_os(self) -> OS:
        pass

    @abstractmethod
    def get_os_version(self) -> str:
        pass

    @abstractmethod
    def get_arch(self) -> Architecture:
        pass


class ManualArchitectureGetter(AbstractArchitectureGetter):
    _os: OS = None
    _os_ver: str = None
    _arch: Architecture = None

    def __init__(self, os: OS, os_ver: str, arch: Architecture):
        self._os = os
        self._os_ver = os_ver
        self._arch = arch

    def get_os(self) -> OS:
        return self._os

    def get_os_version(self) -> str:
        return self._os_ver

    def get_arch(self) -> Architecture:
        return self._arch


class ArchitectureGetter(AbstractArchitectureGetter):
    _os: str = None
    _arch: str = None

    def __init__(self):
        self._os = platform.system()
        self._arch = platform.machine()

    def get_os(self) -> OS:
        return map_to_generic_os(self._os)

    def get_os_version(self) -> str:
        os = self.get_os()
        if os == OS.OSX:
            return platform.mac_ver()[0]

        if os == OS.WINDOWS:
            return platform.version()

        return None

    def get_arch(self) -> Architecture:
        return map_to_generic_arch(self._arch)
