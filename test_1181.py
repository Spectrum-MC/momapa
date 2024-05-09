import unittest
import json

from momapa import parse_manifest, MojangManifest


class TestManifest1181(unittest.TestCase):
    parsed: MojangManifest

    def setUp(self) -> None:
        super().setUp()

        with open('./test_data/1.18.1.json', 'r') as f:
            data = json.load(f)
            self.parsed = parse_manifest(data)

    def test_arguments_str(self):
        self.assertIsNotNone(self.parsed.arguments)
        self.assertIsNotNone(self.parsed.arguments.game)
        self.assertEqual(len(self.parsed.arguments.game), 3)

        arg = self.parsed.arguments.game[0]
        self.assertEqual(
            len(arg.values),
            1,
        )
        self.assertEqual(
            arg.values[0],
            '--username',
        )

    def test_arguments_arr_single_value(self):
        self.assertIsNotNone(self.parsed.arguments)
        self.assertIsNotNone(self.parsed.arguments.game)
        self.assertEqual(len(self.parsed.arguments.game), 3)

        arg = self.parsed.arguments.game[1]
        self.assertEqual(
            len(arg.values),
            1,
        )
        self.assertEqual(
            arg.values[0],
            '--demo',
        )

    def test_arguments_arr_multi_value(self):
        self.assertIsNotNone(self.parsed.arguments)
        self.assertIsNotNone(self.parsed.arguments.game)
        self.assertEqual(len(self.parsed.arguments.game), 3)

        arg = self.parsed.arguments.game[2]
        self.assertEqual(
            len(arg.values),
            4,
        )
        self.assertEqual(arg.values[0], '--width')
        self.assertEqual(arg.values[1], '${resolution_width}')
        self.assertEqual(arg.values[2], '--height')
        self.assertEqual(arg.values[3], '${resolution_height}')

    def test_arguments_rules_default_value(self):
        self.assertIsNotNone(self.parsed.arguments)
        self.assertIsNotNone(self.parsed.arguments.game)
        self.assertEqual(len(self.parsed.arguments.game), 3)

        arg = self.parsed.arguments.game[0]
        self.assertEqual(
            len(arg.rules),
            1,
        )
        self.assertEqual(
            arg.rules[0].action,
            'allow',
        )

    def test_arguments_rules_custom(self):
        self.assertIsNotNone(self.parsed.arguments)
        self.assertIsNotNone(self.parsed.arguments.game)
        self.assertEqual(len(self.parsed.arguments.game), 3)

        arg = self.parsed.arguments.game[1]
        self.assertEqual(
            len(arg.rules),
            1,
        )
        self.assertEqual(
            arg.rules[0].action,
            'allow',
        )
        self.assertDictEqual(
            arg.rules[0].features,
            { 'is_demo_user': True },
        )

if __name__ == '__main__':
    unittest.main()