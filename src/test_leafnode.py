import unittest

from leafnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType


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

    def test_convert_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_convert_bold(self):
        text = TextNode("bold", TextType.BOLD)
        html = text_node_to_html_node(text)
        self.assertEqual(html.tag, "b")
        self.assertEqual(html.value, "bold")
        self.assertEqual(html.props, None)

    def test_convert_italic(self):
        text = TextNode("italic", TextType.ITALIC)
        html = text_node_to_html_node(text)
        self.assertEqual(html.tag, "i")
        self.assertEqual(html.value, "italic")
        self.assertEqual(html.props, None)

    def test_convert_code(self):
        text = TextNode("const three = 3", TextType.CODE)
        html = text_node_to_html_node(text)
        self.assertEqual(html.tag, "code")
        self.assertEqual(html.value, "const three = 3")
        self.assertEqual(html.props, None)

    def test_convert_link(self):
        text = TextNode("example", TextType.LINK, "https://example.com/")
        html = text_node_to_html_node(text)
        self.assertEqual(html.tag, "a")
        self.assertEqual(html.value, "example")
        self.assertEqual(html.props["href"], "https://example.com/")

    def test_convert_image(self):
        text = TextNode("image", TextType.IMAGE,
                        "https://example.com/example.png")
        html = text_node_to_html_node(text)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(html.props["alt"], "image")
        self.assertEqual(html.props["src"], "https://example.com/example.png")

    def test_convert_invalid(self):
        text = TextNode("howdy", "invalid")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text)


if __name__ == "__main__":
    unittest.main()
