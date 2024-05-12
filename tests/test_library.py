from momapa import GameLibrary, OS, Architecture, RuleAction


def test_library_parsestandard():
    lib_dict = {
        "downloads": {
            "artifact": {
                "path": "com/mojang/text2speech/1.17.9/text2speech-1.17.9.jar",
                "sha1": "3cad216e3a7f0c19b4b394388bc9ffc446f13b14",
                "size": 12243,
                "url": "https://url/text2speech-1.17.9.jar",
            }
        },
        "name": "com.mojang:text2speech:1.17.9",
    }

    l = GameLibrary.parse(lib_dict)

    assert l is not None
    assert isinstance(l, GameLibrary)  # Could be an array
    assert l.name == "com.mojang:text2speech:1.17.9"
    assert l.rules is not None
    assert len(l.rules) == 0
    assert l.extract_natives is False
    assert l.is_natives is False
    assert l.artifact is not None

    assert l.artifact.path == "com/mojang/text2speech/1.17.9/text2speech-1.17.9.jar"
    assert l.artifact.hash == "3cad216e3a7f0c19b4b394388bc9ffc446f13b14"
    assert l.artifact.size == 12243
    assert l.artifact.url == "https://url/text2speech-1.17.9.jar"


def test_library_current_norules():
    lib_dict = {
        "downloads": {
            "artifact": {
                "path": "io/netty/netty-transport-native-epoll/4.1.97.Final/netty-transport-native-epoll-4.1.97.Final-linux-aarch_64.jar",
                "sha1": "5514744c588190ffda076b35a9b8c9f24946a960",
                "size": 40427,
                "url": "https://url/netty-transport-native-epoll-4.1.97.Final-linux-aarch_64.jar",
            }
        },
        "name": "io.netty:netty-transport-native-epoll:4.1.97.Final:linux-aarch_64",
    }

    l = GameLibrary.parse(lib_dict)
    assert l is not None
    assert isinstance(l, GameLibrary)
    assert l.name == "io.netty:netty-transport-native-epoll:4.1.97.Final"
    assert l.is_natives is True
    assert l.extract_natives is False

    assert l.artifact is not None
    path = "io/netty/netty-transport-native-epoll/4.1.97.Final/netty-transport-native-epoll-4.1.97.Final-linux-aarch_64.jar"
    assert l.artifact.path == path
    assert l.artifact.hash == "5514744c588190ffda076b35a9b8c9f24946a960"
    assert l.artifact.size == 40427
    assert (
        l.artifact.url
        == "https://url/netty-transport-native-epoll-4.1.97.Final-linux-aarch_64.jar"
    )

    assert l.rules is not None
    assert len(l.rules) == 1

    r = l.rules[0]
    assert r.action == RuleAction.ALLOW
    assert r.features is None
    assert r.os is not None
    assert r.os.get("name") == OS.LINUX
    assert r.os.get("arch") == Architecture.ARM64


def test_library_current_noarch():
    lib_dict = {
        "downloads": {
            "artifact": {
                "path": "org/lwjgl/lwjgl-freetype/3.3.3/lwjgl-freetype-3.3.3-natives-macos.jar",
                "sha1": "1e9b635b5c16b515527b905749be59223e338c4d",
                "size": 1142682,
                "url": "https://url/lwjgl-freetype-3.3.3-natives-macos.jar",
            }
        },
        "name": "org.lwjgl:lwjgl-freetype:3.3.3:natives-macos",
        "rules": [{"action": "allow", "os": {"name": "osx"}}],
    }

    l = GameLibrary.parse(lib_dict)
    assert l is not None
    assert isinstance(l, GameLibrary)
    assert l.name == "org.lwjgl:lwjgl-freetype:3.3.3"
    assert l.is_natives is True
    assert l.extract_natives is False

    assert l.artifact is not None
    assert (
        l.artifact.path
        == "org/lwjgl/lwjgl-freetype/3.3.3/lwjgl-freetype-3.3.3-natives-macos.jar"
    )
    assert l.artifact.hash == "1e9b635b5c16b515527b905749be59223e338c4d"
    assert l.artifact.size == 1142682
    assert l.artifact.url == "https://url/lwjgl-freetype-3.3.3-natives-macos.jar"

    assert l.rules is not None
    assert len(l.rules) == 1

    r = l.rules[0]
    assert r.action == RuleAction.ALLOW
    assert r.features is None
    assert r.os is not None
    assert r.os.get("name") == OS.OSX
    assert r.os.get("arch") == Architecture.AMD64


def test_library_legacy_natives_norules():
    data = {
        "downloads": {
            "artifact": {
                "path": "org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar",
                "sha1": "ee8e57a79300f78294576d87c4a587f8c99402e2",
                "size": 34848,
                "url": "https://url/lwjgl-jemalloc-3.2.2.jar",
            },
            "classifiers": {
                "natives-linux": {
                    "path": "org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2-natives-linux.jar",
                    "sha1": "268c08a150347e04e44ba56e359d62c9b78669df",
                    "size": 156173,
                    "url": "https://url/lwjgl-jemalloc-3.2.2-natives-linux.jar",
                },
                "natives-windows": {
                    "path": "org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2-natives-windows.jar",
                    "sha1": "338b25b99da3ba5f441f6492f2ce2a9c608860ed",
                    "size": 220623,
                    "url": "https://url/lwjgl-jemalloc-3.2.2-natives-windows.jar",
                },
            },
        },
        "name": "org.lwjgl:lwjgl-jemalloc:3.2.2",
        "natives": {"linux": "natives-linux", "windows": "natives-windows"},
        "rules": [{"action": "allow"}, {"action": "disallow", "os": {"name": "osx"}}],
    }

    lib = GameLibrary.parse(data)

    assert lib is not None
    assert not isinstance(lib, GameLibrary)
    assert len(lib) == 3
    assert lib[0].is_natives is False

    assert lib[1].is_natives is True
    assert len(lib[1].rules) == 1
    assert lib[1].rules[0].action == RuleAction.ALLOW
    assert lib[1].rules[0].os.get("name") == OS.LINUX

    assert lib[2].is_natives is True
    assert len(lib[2].rules) == 1
    assert lib[2].rules[0].action == RuleAction.ALLOW
    assert lib[2].rules[0].os.get("name") == OS.WINDOWS


def test_library_legacy_natives_oldosxhack():
    data = {
        "downloads": {
            "artifact": {
                "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209.jar",
                "sha1": "b04f3ee8f5e43fa3b162981b50bb72fe1acabb33",
                "size": 22,
                "url": "https://url/lwjgl-platform-2.9.4-nightly-20150209.jar",
            },
            "classifiers": {
                "natives-linux": {
                    "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                    "sha1": "931074f46c795d2f7b30ed6395df5715cfd7675b",
                    "size": 578680,
                    "url": "https://url/lwjgl-platform-2.9.4-nightly-20150209-natives-linux.jar",
                },
                "natives-osx": {
                    "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                    "sha1": "bcab850f8f487c3f4c4dbabde778bb82bd1a40ed",
                    "size": 426822,
                    "url": "https://url/lwjgl-platform-2.9.4-nightly-20150209-natives-osx.jar",
                },
                "natives-windows": {
                    "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.4-nightly-20150209/lwjgl-platform-2.9.4-nightly-20150209-natives-windows.jar",
                    "sha1": "b84d5102b9dbfabfeb5e43c7e2828d98a7fc80e0",
                    "size": 613748,
                    "url": "https://url/lwjgl-platform-2.9.4-nightly-20150209-natives-windows.jar",
                },
            },
        },
        "extract": {"exclude": ["META-INF/"]},
        "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.4-nightly-20150209",
        "natives": {
            "linux": "natives-linux",
            "osx": "natives-osx",
            "windows": "natives-windows",
        },
        "rules": [{"action": "allow"}, {"action": "disallow", "os": {"name": "osx"}}],
    }

    lib = GameLibrary.parse(data)

    assert lib is not None
    assert not isinstance(lib, GameLibrary)
    assert len(lib) == 3
    assert lib[0].is_natives is False

    assert lib[1].is_natives is True
    assert len(lib[1].rules) == 1
    assert lib[1].rules[0].action == RuleAction.ALLOW
    assert lib[1].rules[0].os.get("name") == OS.LINUX

    assert lib[2].is_natives is True
    assert len(lib[2].rules) == 1
    assert lib[2].rules[0].action == RuleAction.ALLOW
    assert lib[2].rules[0].os.get("name") == OS.WINDOWS