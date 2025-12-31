import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):

    def test_tag(self):
        node = HTMLNode("html")
        self.assertIn("html", node.__repr__())

    def test_value(self):
        node = HTMLNode(None, "value")
        self.assertIn("value", node.__repr__())

    def test_children(self):
        child = HTMLNode("p", "paragraph")
        container = HTMLNode("body", None, [child])
        self.assertIn("paragraph", container.__repr__())

    def test_props(self):
        node = HTMLNode("a", None, None, {"href": "https://example.com/"})
        self.assertIn("href", node.__repr__())
        self.assertIn("example", node.__repr__())

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("a", None, None, {
            "href": "https://example.com/",
            "class": "fake",
        })
        self.assertEqual('href="https://example.com/" class="fake"',
                         node.props_to_html())


if __name__ == "__main__":
    unittest.main()
