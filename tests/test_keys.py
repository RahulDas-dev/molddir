import unittest

from molddir.keys import KeyBuilder


class TestKeyBuilder(unittest.TestCase):
    def setUp(self):
        self.default_encoder_key = """@@@@@@@{file_path}@@@@@@@\n{code_block}\n=======\n"""
        self.default_decoder_key = r"""@@@@@@@(?P<file_path>.*?)@@@@@@@\n(?P<code_block>.*?)\n=======\n"""
        self.custom_encoder_key = """CUSTOM@@@{file_path}@@@CUSTOM\n{code_block}\nCUSTOM===\n"""
        self.custom_decoder_key = r"""CUSTOM@@@(?P<file_path>.*?)@@@CUSTOM\n(?P<code_block>.*?)\nCUSTOM===\n"""

    def test_default_initialization(self):
        kb = KeyBuilder()
        self.assertEqual(kb.encoder_key, self.default_encoder_key)
        self.assertEqual(kb.decoder_key, self.default_decoder_key)

    def test_custom_initialization(self):
        kb = KeyBuilder(encoder_key=self.custom_encoder_key, decoder_key=self.custom_decoder_key)
        self.assertEqual(kb.encoder_key, self.custom_encoder_key)
        self.assertEqual(kb.decoder_key, self.custom_decoder_key)

    def test_encoder_key_property(self):
        kb = KeyBuilder()
        self.assertEqual(kb.encoder_key, self.default_encoder_key)

    def test_decoder_key_property(self):
        kb = KeyBuilder()
        self.assertEqual(kb.decoder_key, self.default_decoder_key)

    def test_validate_keys_success(self):
        kb = KeyBuilder()
        self.assertTrue(kb._validate_keys())

    def test_validate_keys_failure(self):
        invalid_decoder_key = r"""@@@@INVALID@@@(?P<file_path>.*?)@@@@@@@\n(?P<code_block>.*?)\nINVALID=======\n"""
        with self.assertRaises(ValueError):
            KeyBuilder(decoder_key=invalid_decoder_key)


if __name__ == "__main__":
    unittest.main()
