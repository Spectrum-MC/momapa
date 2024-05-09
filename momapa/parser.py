from typing import Optional
from datetime import datetime

from .models import *

def _parse_datetime(isoformat: Optional[str]) -> Optional[datetime]:
    if not isoformat:
        return None

    return datetime.fromisoformat(isoformat)

def _parse_jar_file(downloads: dict, key: str) -> JarFile:
    file = downloads.get(key)
    if not file:
        return None

    jf = JarFile()
    jf.url = file.get('url')
    jf.size = file.get('size')
    jf.hash = file.get('sha1')

    return jf

def _parse_new_arguments(manifest_arguments: dict):
    args = {'game': [], 'jvm': []}

    for man_arg_key in args.keys():
        for man_arg in manifest_arguments.get(man_arg_key, []):
            if isinstance(man_arg, str):
                arg = Argument([man_arg], [Rule('allow')])
            else:
                man_arg_val = man_arg.get('value')

                arg = Argument(
                    [man_arg_val] if isinstance(man_arg_val, str) else man_arg_val,
                    [
                        Rule(
                            x.get('action'),
                            x.get('features'),
                            x.get('os')
                        )
                        for x in man_arg.get('rules', [])
                    ]
                )

            args[man_arg_key].append(arg)

    return GameArgumentSet(
        args.get('game'),
        args.get('jvm'),
    )

def _parse_legacy_arguments(mc_args: str):
    return GameArgumentSet(
        [
            Argument([x], [Rule('allow')])
            for x in mc_args.split(' ')
        ],
        [],
    )


def parse_manifest(data: dict) -> MojangManifest:
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

    #region Parsing jar files
    downloads = data.get('downloads', {})

    gd = GameDownloads()
    gd.client = _parse_jar_file(downloads, 'client')
    gd.client_mappings = _parse_jar_file(downloads, 'client_mappings')
    gd.server = _parse_jar_file(downloads, 'server')
    gd.server_mappings = _parse_jar_file(downloads, 'server_mappings')

    manifest.jar_files = gd
    #endregion

    #region Parsing assets
    assets = None
    assets_idx = data.get('assetIndex')

    if assets_idx:
        assets = AssetIndex()
        assets.id = assets_idx.get('id')
        assets.hash = assets_idx.get('sha1')
        assets.size = assets_idx.get('size')
        assets.total_size = assets_idx.get('totalSize')
        assets.url = assets_idx.get('url')

    manifest.assets = assets
    #endregion

    #region Parsing arguments
    if 'arguments' in data:
        manifest.arguments = _parse_new_arguments(data.get('arguments', {}))
    elif 'minecraftArguments' in data:
        manifest.arguments = _parse_legacy_arguments(data.get('minecraftArguments'))
    #endregion

    #region Parsing Java version
    jv = None
    data_jv = data.get('javaVersion')
    if data_jv:
        jv = JavaVersion()
        jv.component = data_jv.get('component')
        jv.major_version = data_jv.get('majorVersion')

    manifest.java_version = jv
    #endregion

    return manifest