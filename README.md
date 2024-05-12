# MOjangMAnifestPArser

This simple lib takes a Mojang Minecraft manifest and parse it to a set of useful classes in Python.

## Setup

```sh
$ pip install momapa
```

## Usage

This library exposes one main function: `MojangManifest.parse`. You give it a `dict` from Mojang's manifest and it parses it to some simple classes and try to standardize it so that you don't have to worry about differences between legacy manifests and newer ones.

It also helps you validate the rules in the arguments and the libraries to know exactly which one you need to apply for a given OS/Arch/feature-set

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

Note that you can also validate the rules (for Game/JVM arguments and libraries):
```python
from momapa import MojangManifest, RuleValidator, ArchitectureGetter, ManualArchitectureGetter

manifest = MojangManifest.parse(data)
rules = manifest.libraries[x].rules

# Check if a single rule matches
rv = RuleValidator(
    ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64), # Manually feed the system info
    { 'is_demo': False, 'has_custom_resolution': False },
)
print(rv.rule_matches(rules[0]))

# Validate the whole ruleset (Returns the action to do)
rv = RuleValidator(
    ArchitectureGetter(), # Fetches the system info by itself
    { 'is_demo': False, 'has_custom_resolution': False },
)
print(rv.validate_ruleset(rules)) # Returns either "allow" or "disallow"
```

## Status
- [x] Parsing generic parts of the manifest
- [x] Parsing jar file section
- [x] Parsing asset manifest
- [x] Parsing arguments (Legacy)
- [x] Parsing arguments (1.12+)
- [x] Parsing java version manifest
- [x] Parsing libraries (Legacy, not 100% accurate though)
- [x] Parsing libraries (1.20.4+)
- [x] Parsing the "Logging" file
- [x] Rule validator
- [x] Ruleset validator

This library has been tested on versions up to 1.20.6. If there is any issue parsing newer versions, please make an issue to tell me that something has changed and need to be taken care of.

The only things I'm not quite sure it works as intended is on old versions of the game, there are some rule for some specific libraries to blacklist them on OSX 10.5.x. This is neither unit-tested not tested at all.
```json
[
    { "action": "allow" },
    {
      "action": "disallow",
      "os": { "name": "osx", "version": "^10\\.5\\.\\d$" }
    }
],
```

## License
> MoMaPa - Mojang Manifest Parser
> Copyright (C) 2024 - Oxodao
>
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <https://www.gnu.org/licenses/>.
