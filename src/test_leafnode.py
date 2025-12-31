import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "howdy")
        self.assertEqual("howdy", node.to_html())

    def test_to_html_no_props(self):
        node = LeafNode("p", "howdy")
        self.assertEqual("<p>howdy</p>", node.to_html())

    def test_to_html(self):
        node = LeafNode("p", "howdy", {"class": "fake"})
        self.assertEqual('<p class="fake">howdy</p>', node.to_html())


if __name__ == "__main__":
    unittest.main()
