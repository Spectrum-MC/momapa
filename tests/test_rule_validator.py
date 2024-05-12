from momapa import Rule, RuleValidator, ManualArchitectureGetter, OS, Architecture, RuleAction


def test_validate_single_empty():
    r = Rule(RuleAction.ALLOW)
    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is True


def test_validate_single_feature():
    r = Rule(RuleAction.ALLOW, {'is_demo': True})
    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is False

    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64),
        { 'is_demo': True, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is True


def test_validate_single_os_nameonly():
    r = Rule(RuleAction.ALLOW, None, {
        'name': OS.WINDOWS,
    })

    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is True

    rv = RuleValidator(
        ManualArchitectureGetter(OS.LINUX, '10.0.2204', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is False


def test_validate_single_os_nameandversion():
    r = Rule(RuleAction.ALLOW, None, {
        'name': OS.WINDOWS,
        'version': '^10\\.',
    })

    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is True

    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '7', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is False

    rv = RuleValidator(
        ManualArchitectureGetter(OS.LINUX, '10.0.0', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is False

def test_validate_single_os_arch():
    r = Rule(RuleAction.ALLOW, None, {
        'arch': Architecture.AMD64,
    })

    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is True

    rv = RuleValidator(
        ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.ARM64),
        { 'is_demo': False, 'has_custom_resolution': False },
    )

    res = rv.rule_matches(r)
    assert res is False