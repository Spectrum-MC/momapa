import re
from typing import List

from .os import AbstractArchitectureGetter, RuleAction
from .rule import Rule


class RuleValidator:
    _arch_getter: AbstractArchitectureGetter
    _feature_set: dict

    def __init__(self, arch_getter: AbstractArchitectureGetter, feature_set: dict):
        self._arch_getter = arch_getter
        self._feature_set = feature_set

    def rule_matches(self, rule: Rule) -> bool:
        if not rule.features and not rule.os:
            return True

        matches = True
        if rule.features:
            for f, v in rule.features.items():
                matches = matches and self._feature_set.get(f) == v

        if rule.os:
            os_name = rule.os.get('name')
            os_version = rule.os.get('version')
            os_arch = rule.os.get('arch')

            if matches and os_name:
                matches = matches and (self._arch_getter.get_os() == os_name)

            if matches and os_version:
                matches = matches and bool(re.match(
                    os_version,
                    self._arch_getter.get_os_version()
                ))

            if matches and os_arch:
                matches = matches and (self._arch_getter.get_arch() == os_arch)

        return matches

    def validate_ruleset(self, rules: List[Rule]) -> RuleAction:
        action = RuleAction.ALLOW if len(rules) == 0 else RuleAction.DISALLOW

        for r in rules:
            if not self.rule_matches(r):
                continue

            action = r.action

        return action
