from momapa import Argument, GameArgumentSet, RuleAction

def test_argument_singlestring():
    arg_str = '--username'

    ga = Argument.parse(arg_str)

    assert ga is not None

    assert len(ga.values) == 1
    assert len(ga.rules) == 1

    assert ga.values[0] == '--username'

    # Testing that it automatically added
    # a rule with only the allow action
    assert ga.rules[0].action == RuleAction.ALLOW
    assert ga.rules[0].features is None
    assert ga.rules[0].os is None

def test_argument_singledict():
    arg_str = {
        'value': '--demo',
        'rules': [
            {
                'action': 'allow',
                'features': {
                    'is_demo_user': True,
                }
            }
        ]
    }

    ga = Argument.parse(arg_str)

    assert ga is not None

    assert len(ga.values) == 1
    assert len(ga.rules) == 1

    assert ga.values[0] == '--demo'
    assert ga.rules[0].action == RuleAction.ALLOW
    # Testing that this is a real parsed rule 
    # and not a "allow" added automatically by itself
    assert ga.rules[0].features is not None

def test_argument_multidict():
    arg_str = {
        'value': [
            '--width',
            '${resolution_width}',
            '--height',
            '${resolution_height}'
        ],
        'rules': [
            {
                'action': 'allow',
                'features': {
                    'has_custom_resolution': True,
                }
            }
        ]
    }

    ga = Argument.parse(arg_str)

    assert ga is not None

    assert len(ga.values) == 4
    assert len(ga.rules) == 1

    assert ga.values[0] == '--width'
    assert ga.values[1] == '${resolution_width}'
    assert ga.values[2] == '--height'
    assert ga.values[3] == '${resolution_height}'

    assert ga.rules[0].action == RuleAction.ALLOW
    # Testing that this is a real parsed rule 
    # and not a "allow" added automatically by itself
    assert ga.rules[0].features is not None

def test_gameargumentset_valid():
    gas_dict = {
        'game': [
            '--username',
        ],
        'jvm': [
            '-XstartOnFirstThread',
            {
                'value': [
                    '-Dos.name=Windows 10',
                    '-Dos.version=10.0',
                ],
                'rules': [
                    {
                        'action': 'allow',
                        'os': {
                            'name': 'windows',
                            'version': '^10\\.'
                        }
                    }
                ]
            }
        ]
    }

    gas = GameArgumentSet.parse(gas_dict)
    assert gas is not None

    assert len(gas.game) == 1
    assert len(gas.jvm) == 2

    assert len(gas.game[0].values) == 1
    assert gas.game[0].values[0] == '--username'

    assert len(gas.jvm[0].values) == 1
    assert gas.jvm[0].values[0] == '-XstartOnFirstThread'

def test_gameargumentset_legacy():
    gas_val = '--username ${auth_player_name} --session ${auth_session} --version ${version_name} --gameDir ${game_directory} --assetsDir ${game_assets}'
    gas = GameArgumentSet.parse_legacy(gas_val)

    assert gas is not None
    assert len(gas.jvm) == 0
    assert len(gas.game) == 10

    assert len(gas.game[0].values) == 1
    assert gas.game[0].values[0] == '--username'

    assert len(gas.game[0].rules) == 1
    assert gas.game[0].rules[0].action == RuleAction.ALLOW
    assert gas.game[0].rules[0].features is None
    assert gas.game[0].rules[0].os is None

    assert len(gas.game[1].values) == 1
    assert gas.game[1].values[0] == '${auth_player_name}'

    assert len(gas.game[1].rules) == 1
    assert gas.game[1].rules[0].action == RuleAction.ALLOW
    assert gas.game[1].rules[0].features is None
    assert gas.game[1].rules[0].os is None

def test_gameargumentset_notfound():
    # Not sure this is what we want
    # We maybe want a GAS but with empty array for
    # both JVM & Game ?
    gas = GameArgumentSet.parse(None)
    assert gas is None

def test_gameargumentset_legacy_notfound():
    gas_val = None
    gas = GameArgumentSet.parse_legacy(gas_val)
    assert gas is None