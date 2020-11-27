import unittest

from main import replace_ids


class TestValuesReplacer(unittest.TestCase):
    def test_replace_ids(self):
        text = 'Asd %idf% -> %id% feg'
        sample = 'Asd 2345 -> 1234 feg'
        text = replace_ids(text, 1234, lambda task_id: 2345)
        assert text == sample

    def test_replace_ids_wrong_sample(self):
        text = 'Asd %idf% -> %id% feg'
        sample = 'Asd 2345 -> 12343 feg'
        text = replace_ids(text, 1234, lambda task_id: 2345)
        assert text != sample
