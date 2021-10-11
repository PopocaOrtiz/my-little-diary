import unittest
from tags import detect_tags


class TestTags(unittest.TestCase):

    def test_detect_tags(self):
        entry_contents = {
            '#one lorem #two ipsum #three': ['one','two','three'],
            ' #two lorem #one #three ipsum ': ['two', 'one', 'three'],
            ' #one #two #three' : ['one','two','three'],
            ' #one #three #two #tag#invalid invalid#tag l': ['one','three','two', 'tag'],
        }

        for content in entry_contents:

            list_of_tags = entry_contents[content]

            with self.subTest(i=content):
                self.assertEqual(list_of_tags, detect_tags(content))


if __name__ == '__main__':
    unittest.main()
