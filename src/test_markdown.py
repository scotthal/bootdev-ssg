import unittest

from markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestMarkdown(unittest.TestCase):

    def test_split_bold(self):
        input = TextNode("string with **bold** text", TextType.PLAIN)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.BOLD)
        self.assertEqual(output[1].text, "bold")
        self.assertEqual(output[2].text_type, TextType.PLAIN)

    def test_split_italic(self):
        input = TextNode("string with _italic_ text", TextType.PLAIN)
        output = split_nodes_delimiter([input], "_", TextType.ITALIC)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.ITALIC)
        self.assertEqual(output[1].text, "italic")
        self.assertEqual(output[2].text_type, TextType.PLAIN)

    def test_split_code(self):
        input = TextNode("string with `code` text", TextType.PLAIN)
        output = split_nodes_delimiter([input], "`", TextType.CODE)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.CODE)
        self.assertEqual(output[1].text, "code")
        self.assertEqual(output[2].text_type, TextType.PLAIN)

    def test_split_begin(self):
        input = TextNode("_italic_ at beginning", TextType.PLAIN)
        output = split_nodes_delimiter([input], "_", TextType.ITALIC)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[0].text, "")
        self.assertEqual(output[1].text_type, TextType.ITALIC)
        self.assertEqual(output[1].text, "italic")
        self.assertEqual(output[2].text_type, TextType.PLAIN)

    def test_split_end(self):
        input = TextNode("string ends with _italic_", TextType.PLAIN)
        output = split_nodes_delimiter([input], "_", TextType.ITALIC)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.ITALIC)
        self.assertEqual(output[1].text, "italic")
        self.assertEqual(output[2].text_type, TextType.PLAIN)
        self.assertEqual(output[2].text, "")

    def test_split_multi(self):
        input = TextNode("multiple **bold** parts in **this** string",
                         TextType.PLAIN)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.BOLD)
        self.assertEqual(output[2].text_type, TextType.PLAIN)
        self.assertEqual(output[3].text_type, TextType.BOLD)
        self.assertEqual(output[4].text_type, TextType.PLAIN)

    def test_split_not_text(self):
        input = TextNode("link", TextType.LINK, "https://example.com/")
        output = split_nodes_delimiter([input], "_", TextType.ITALIC)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text_type, TextType.LINK)

    def test_split_no_delimiter(self):
        input = TextNode("no bold text here", TextType.PLAIN)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text_type, TextType.PLAIN)

    def test_split_multi_list(self):
        input1 = TextNode("some _italic_ text", TextType.PLAIN)
        input2 = TextNode("more _italic_ text", TextType.PLAIN)
        output = split_nodes_delimiter([input1, input2], "_", TextType.ITALIC)
        self.assertEqual(len(output), 6)
        self.assertEqual(output[1].text_type, TextType.ITALIC)
        self.assertEqual(output[4].text_type, TextType.ITALIC)

    def test_split_unbalanced(self):
        input = TextNode("this `code never ends", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([input], "`", TextType.CODE)


if __name__ == "__main__":
    unittest.main()
