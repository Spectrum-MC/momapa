import unittest
import json

from momapa import parse_manifest, MojangManifest


class TestManifestLegacy(unittest.TestCase):
    parsed: MojangManifest

    def setUp(self) -> None:
        super().setUp()

        with open('./test_data/a1.2.1.json', 'r') as f:
            data = json.load(f)
            self.parsed = parse_manifest(data)

    def test_arguments(self):
        self.assertIsNotNone(self.parsed.arguments)

        self.assertIsNotNone(self.parsed.arguments.jvm)
        self.assertEqual(len(self.parsed.arguments.jvm), 0)

        self.assertIsNotNone(self.parsed.arguments.game)
        self.assertEqual(len(self.parsed.arguments.game), 6)

        arg = self.parsed.arguments.game[0]
        self.assertEqual(
            len(arg.values),
            1,
        )
        self.assertEqual(
            arg.values[0],
            '${auth_player_name}',
        )
        self.assertEqual(
            len(arg.rules),
            1,
        )
        self.assertEqual(
            arg.rules[0].action,
            'allow',
        )

if __name__ == '__main__':
    unittest.main()