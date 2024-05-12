from momapa import Rule, OS, Architecture, RuleAction

def test_rule_notfound():
    r = Rule.parse(None)
    assert r is None

def test_rule_noconditions():
    r_dict = {
        'action': 'allow',
    }

    r = Rule.parse(r_dict)
    assert r is not None
    assert r.action == RuleAction.ALLOW
    assert r.features is None
    assert r.os is None

def test_rule_features():
    r_dict = {
        'action': 'disallow',
        'features': {
            'has_custom_resolution': True,
        },
    }

    r = Rule.parse(r_dict)
    assert r is not None
    assert r.action == RuleAction.DISALLOW
    assert r.os is None
    assert r.features is not None
    assert r.features.get('has_custom_resolution') is True

def test_rule_os():
    r_dict = {
        'action': 'disallow',
        'os': {
            'name': 'windows',
            'arch': 'arm64',
            'version': '^10\\.'
        },
    }

    r = Rule.parse(r_dict)
    assert r is not None
    assert r.action == RuleAction.DISALLOW
    assert r.features is None
    assert r.os is not None
    assert r.os.get('name') == OS.WINDOWS
    assert r.os.get('arch') == Architecture.ARM64
    assert r.os.get('version') == '^10\\.'