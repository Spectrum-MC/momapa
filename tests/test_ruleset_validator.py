from momapa import Rule, RuleAction, ManualArchitectureGetter, RuleValidator, OS, Architecture


def test_ruleset_allow_except_osx():
    ruleset = [
        Rule(RuleAction.ALLOW),
        Rule(RuleAction.DISALLOW, None, {
            'name': OS.OSX,
        })
    ]

    rv = RuleValidator(ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64), {})
    res = rv.validate_ruleset(ruleset)
    assert res == RuleAction.ALLOW

    rv = RuleValidator(ManualArchitectureGetter(OS.OSX, '10.14', Architecture.AMD64), {})
    res = rv.validate_ruleset(ruleset)
    assert res == RuleAction.DISALLOW

def test_ruleset_allow_only_osx():
    ruleset = [
        Rule(RuleAction.ALLOW, None, {
            'name': OS.OSX,
        })
    ]

    rv = RuleValidator(ManualArchitectureGetter(OS.WINDOWS, '10.0.2204', Architecture.AMD64), {})
    res = rv.validate_ruleset(ruleset)
    assert res == RuleAction.DISALLOW

    rv = RuleValidator(ManualArchitectureGetter(OS.OSX, '10.14', Architecture.AMD64), {})
    res = rv.validate_ruleset(ruleset)
    assert res == RuleAction.ALLOW