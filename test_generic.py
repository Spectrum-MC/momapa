import unittest
import json

from momapa import parse_manifest, MojangManifest


class TestManifestLegacy(unittest.TestCase):
    parsed_legacy: MojangManifest
    parsed_1181: MojangManifest

    def setUp(self) -> None:
        super().setUp()

        with open('./test_data/a1.2.1.json', 'r') as f:
            data = json.load(f)
            self.parsed_legacy = parse_manifest(data)

        with open('./test_data/1.18.1.json', 'r') as f:
            data = json.load(f)
            self.parsed_1181 = parse_manifest(data)

    def test_generic_values(self):
        self.assertEqual(
            self.parsed_legacy.id,
            'a1.2.1',
        )

        self.assertEqual(
            self.parsed_legacy.type,
            'old_alpha',
        )

        self.assertEqual(
            self.parsed_legacy.time.strftime('%Y-%m-%d %H:%M:%S'),
            '2010-11-04 22:00:00',
        )

        self.assertEqual(
            self.parsed_legacy.release_time.strftime('%Y-%m-%d %H:%M:%S'),
            '2010-11-04 22:00:00',
        )

        self.assertEqual(
            self.parsed_legacy.main_class,
            'net.minecraft.launchwrapper.Launch',
        )

        self.assertEqual(
            self.parsed_legacy.minimum_launcher_version,
            7,
        )

        self.assertEqual(
            self.parsed_legacy.compliance_level,
            0,
        )

    def __test_version(self, version, expectedUrl, expectedHash, expectedSize):
        self.assertIsNotNone(version)
        self.assertEqual(
            version.url,
            expectedUrl,
        )

        self.assertEqual(
            version.hash,
            expectedHash,
        )

        self.assertEqual(
            version.size,
            expectedSize,
        )

    def test_downloads_legacy(self):
        self.assertIsNotNone(self.parsed_legacy.jar_files)

        self.__test_version(
            self.parsed_legacy.jar_files.client,
            'url of the client jar file',
            'e4226f9ba622634e3101681bc641eec7ee9e72fd',
            1053508,
        )

        self.assertIsNone(self.parsed_legacy.jar_files.client_mappings)
        self.assertIsNone(self.parsed_legacy.jar_files.server)
        self.assertIsNone(self.parsed_legacy.jar_files.server_mappings)

    def test_downloads_1181(self):
        self.assertIsNotNone(self.parsed_1181.jar_files)

        self.__test_version(
            self.parsed_1181.jar_files.client,
            'url of the client jar file',
            '7e46fb47609401970e2818989fa584fd467cd036',
            20042090,
        )

        self.__test_version(
            self.parsed_1181.jar_files.client_mappings,
            'url of the client mapping file',
            '99ade839eacf69b8bed88c91bd70ca660aee47bb',
            6611464,
        )

        self.__test_version(
            self.parsed_1181.jar_files.server,
            'url of the server jar file',
            '125e5adf40c659fd3bce3e66e67a16bb49ecc1b9',
            46324407,
        )

        self.__test_version(
            self.parsed_1181.jar_files.server_mappings,
            'url of the server mapping file',
            '9717df2acd926bd4a9a7b2ce5f981bb7e4f7f04a',
            5115621,
        )
 
    def test_asset_index(self):
        self.assertIsNotNone(self.parsed_legacy.assets)
        self.assertEqual(
            self.parsed_legacy.assets.id,
            'pre-1.6',
        )

        self.assertEqual(
            self.parsed_legacy.assets.url,
            'url of the assets',
        )

        self.assertEqual(
            self.parsed_legacy.assets.hash,
            '3d8e55480977e32acd9844e545177e69a52f594b',
        )

        self.assertEqual(
            self.parsed_legacy.assets.size,
            74091,
        )

        self.assertEqual(
            self.parsed_legacy.assets.total_size,
            49505710,
        )

    def test_java_version(self):
        self.assertIsNotNone(self.parsed_legacy.java_version)
        self.assertEqual(
            self.parsed_legacy.java_version.component,
            'jre-legacy'
        )
        self.assertEqual(
            self.parsed_legacy.java_version.major_version,
            8,
        )

if __name__ == '__main__':
    unittest.main()