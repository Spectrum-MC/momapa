# MOjangMAnifestPArser

This simple lib takes a Mojang Minecraft manifest and parse it to a set of useful classes in Python.

This is targetted at launchers so we drop non-launcher related things

## Usage

This library exposes one main function: `parse_manifest`. You give it a `dict` from Mojang's manifest and it parses it to some simple classes and try to standardize it so that you don't have to worry about differences between legacy manifests and newer ones.

Exemple usage:
```python
import requests
from momapa import MojangManifest

data = requests.get('https://piston-meta.mojang.com/mc/game/version_manifest_v2.json').json()

for v in data.get('versions'):
    if v.get('id') == '1.20.1':
        data = requests.get(v.get('url')).json()
        manifest = MojangManifest.parse(data)

        print(manifest.id)
        print(manifest.jar_files.server.hash)
```

## Status
- [x] Parsing generic parts of the manifest
- [x] Parsing jar file section
- [x] Parsing asset manifest
- [x] Parsing arguments (Legacy)
- [x] Parsing arguments (1.12+)
- [x] Parsing java version manifest
- [~] Parsing libraries (Legacy)
- [x] Parsing libraries (1.20.4+)
- [ ] Rule validator
- [ ] Ruleset validator