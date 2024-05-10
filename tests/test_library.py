from momapa import GameLibrary, OS, Architecture


d2 = {
    "downloads": {
        "classifiers": {
            "natives-linux": {
                "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-linux.jar",
                "sha1": "d898a33b5d0a6ef3fed3a4ead506566dce6720a5",
                "size": 578539,
                "url": "https://url/lwjgl-platform-2.9.2-nightly-20140822-natives-linux.jar",
            },
            "natives-osx": {
                "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-osx.jar",
                "sha1": "79f5ce2fea02e77fe47a3c745219167a542121d7",
                "size": 468116,
                "url": "https://url/lwjgl-platform-2.9.2-nightly-20140822-natives-osx.jar",
            },
            "natives-windows": {
                "path": "org/lwjgl/lwjgl/lwjgl-platform/2.9.2-nightly-20140822/lwjgl-platform-2.9.2-nightly-20140822-natives-windows.jar",
                "sha1": "78b2a55ce4dc29c6b3ec4df8ca165eba05f9b341",
                "size": 613680,
                "url": "https://url/lwjgl-platform-2.9.2-nightly-20140822-natives-windows.jar",
            },
        }
    },
    "extract": {"exclude": ["META-INF/"]},
    "name": "org.lwjgl.lwjgl:lwjgl-platform:2.9.2-nightly-20140822",
    "natives": {
        "linux": "natives-linux",
        "osx": "natives-osx",
        "windows": "natives-windows",
    },
    "rules": [{"action": "allow", "os": {"name": "osx"}}],
}

d3 = {
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
    assert l.name == 'io.netty:netty-transport-native-epoll:4.1.97.Final'
    assert l.is_natives is True
    assert l.extract_natives is False

    assert l.artifact is not None
    assert l.artifact.path == 'io/netty/netty-transport-native-epoll/4.1.97.Final/netty-transport-native-epoll-4.1.97.Final-linux-aarch_64.jar'
    assert l.artifact.hash == '5514744c588190ffda076b35a9b8c9f24946a960'
    assert l.artifact.size == 40427
    assert l.artifact.url == 'https://url/netty-transport-native-epoll-4.1.97.Final-linux-aarch_64.jar'

    assert l.rules is not None
    assert len(l.rules) == 1

    r = l.rules[0]
    assert r.action == 'allow'
    assert r.features is None
    assert r.os is not None
    assert r.os.get('name') == OS.LINUX
    assert r.os.get('arch') == Architecture.ARM64