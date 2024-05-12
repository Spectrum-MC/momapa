from dataclasses import dataclass
from typing import List, Optional, Self

from .os import RuleAction
from .rule import Rule


@dataclass
class Argument:
    values: List[str]
    rules: List[Rule]

    @staticmethod
    def parse(arg) -> Optional[Self]:
        if isinstance(arg, str):
            return Argument([arg], [Rule(RuleAction.ALLOW)])

        values = arg.get('value')
        if not values:
            return None

        if isinstance(values, str):
            values = [values]

        rules = []
        for r in arg.get('rules', []):
            rules.append(Rule.parse(r))

        return Argument(values, rules)


@dataclass
class GameArgumentSet:
    game: List[Argument]
    jvm: List[Argument]

    @staticmethod
    def parse(arguments: dict) -> Optional[Self]:
        if not arguments:
            return None

        game_args = []
        jvm_args = []

        for arg in arguments.get('game', []):
            game_args.append(Argument.parse(arg))

        for arg in arguments.get('jvm', []):
            jvm_args.append(Argument.parse(arg))

        return GameArgumentSet(
            game_args,
            jvm_args,
        )

    @staticmethod
    def parse_legacy(arguments: str) -> Optional[Self]:
        if not arguments:
            return None

        return GameArgumentSet([
            Argument([x], [Rule(RuleAction.ALLOW)])
            for x in arguments.split(' ')
        ], [])
