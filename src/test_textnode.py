import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_unequal_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a boring node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_unequal_type(self):
        node1 = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_unequal_url(self):
        node1 = TextNode("This is a text node", TextType.LINK,
                         "https://example.com/")
        node2 = TextNode("This is a text node", TextType.LINK,
                         "https://example.com/example")
        self.assertNotEqual(node1, node2)

    def test_none_url(self):
        node1 = TextNode("This is a text node", TextType.LINK,
                         "https://example.com/")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
