import unittest

from markdown import extract_markdown_images
from markdown import extract_markdown_links
from markdown import split_nodes_delimiter
from markdown import split_nodes_image
from markdown import split_nodes_link
from markdown import text_to_textnodes
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

    def test_split_begin_end(self):
        input = TextNode("_italic only_", TextType.PLAIN)
        output = split_nodes_delimiter([input], "_", TextType.ITALIC)
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[0].text, "")
        self.assertEqual(output[1].text_type, TextType.ITALIC)
        self.assertEqual(output[1].text, "italic only")
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

    def test_extract_images_basic(self):
        output = extract_markdown_images(
            "![alt text](https://example.com/image.png)")
        self.assertEqual(output,
                         [("alt text", "https://example.com/image.png")])

    def test_extract_images_link(self):
        output = extract_markdown_images("[link text](https://example.com/)")
        self.assertEqual(output, [])

    def test_extract_images_no_image(self):
        output = extract_markdown_images("no images here!")
        self.assertEqual(output, [])

    def test_extract_images_empty(self):
        output = extract_markdown_images("")
        self.assertEqual(output, [])

    def test_extract_images_none(self):
        with self.assertRaises(TypeError):
            extract_markdown_images(None)

    def multi_image_text(self):
        result = "![alt text](https://example.com/alt.png)"
        result += " [link text](https://example.com/)"
        result += " I like cheese!"
        result += " ![cheese text](https://example.com/cheese.png)"
        return result

    def test_extract_images_multiple(self):
        output = extract_markdown_images(self.multi_image_text())
        self.assertEqual(output, [
            ("alt text", "https://example.com/alt.png"),
            ("cheese text", "https://example.com/cheese.png"),
        ])

    def test_extract_links_basic(self):
        output = extract_markdown_links("[link text](https://example.com/)")
        self.assertEqual(output, [("link text", "https://example.com/")])

    def test_extract_links_image(self):
        output = extract_markdown_links(
            "![alt text](https://example.com/image.png)")
        self.assertEqual(output, [])

    def test_extract_links_no_links(self):
        output = extract_markdown_links("[no links in here]")
        self.assertEqual(output, [])

    def test_extract_links_empty(self):
        output = extract_markdown_links("")
        self.assertEqual(output, [])

    def test_extract_links_none(self):
        with self.assertRaises(TypeError):
            extract_markdown_links(None)

    def multi_link_text(self):
        result = "[alt text](https://example.com/alt.png)"
        result += " I like cheese!"
        result += " ![cheese text](https://example.com/cheese.png)"
        result += " [cheese text 2](https://example.com/cheese2.png)"
        return result

    def test_extract_links_multiple(self):
        output = extract_markdown_links(self.multi_link_text())
        self.assertEqual(output, [
            ("alt text", "https://example.com/alt.png"),
            ("cheese text 2", "https://example.com/cheese2.png"),
        ])

    def test_split_image(self):
        input = TextNode(self.multi_image_text(), TextType.PLAIN)
        output = split_nodes_image([input])
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.IMAGE)
        self.assertEqual(output[1].text, "alt text")
        self.assertEqual(output[1].url, "https://example.com/alt.png")
        self.assertEqual(output[2].text_type, TextType.PLAIN)
        self.assertEqual(output[3].text_type, TextType.IMAGE)
        self.assertEqual(output[3].text, "cheese text")
        self.assertEqual(output[3].url, "https://example.com/cheese.png")
        self.assertEqual(output[4].text_type, TextType.PLAIN)

    def test_split_image_no_image(self):
        input = TextNode("(no images in here)", TextType.PLAIN)
        output = split_nodes_image([input])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text_type, TextType.PLAIN)

    def test_split_image_empty(self):
        output = split_nodes_image([])
        self.assertEqual(len(output), 0)

    def test_split_image_not_plain(self):
        input = TextNode("bold text", TextType.BOLD)
        output = split_nodes_image([input])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text_type, TextType.BOLD)

    def test_split_link(self):
        input = TextNode(self.multi_link_text(), TextType.PLAIN)
        output = split_nodes_link([input])
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[1].text_type, TextType.LINK)
        self.assertEqual(output[1].text, "alt text")
        self.assertEqual(output[1].url, "https://example.com/alt.png")
        self.assertEqual(output[2].text_type, TextType.PLAIN)
        self.assertEqual(output[3].text_type, TextType.LINK)
        self.assertEqual(output[3].text, "cheese text 2")
        self.assertEqual(output[3].url, "https://example.com/cheese2.png")
        self.assertEqual(output[4].text_type, TextType.PLAIN)

    def test_split_link_no_link(self):
        input = TextNode("[no links here]", TextType.PLAIN)
        output = split_nodes_link([input])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text_type, TextType.PLAIN)

    def test_split_link_empty(self):
        output = split_nodes_link([])
        self.assertEqual(len(output), 0)

    def test_split_link_not_plain(self):
        input = TextNode("bold text", TextType.BOLD)
        output = split_nodes_link([input])
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text_type, TextType.BOLD)

    def all_type_text(self):
        result = "This is"
        result += " **text**"
        result += " with an"
        result += " _italic_"
        result += " word and a"
        result += " `code block`"
        result += " and an"
        result += " ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        result += " and a"
        result += " [link](https://boot.dev)"
        return result

    def test_textnodes(self):
        output = text_to_textnodes(self.all_type_text())
        self.assertEqual(len(output), 11)
        self.assertEqual(output[0].text_type, TextType.PLAIN)
        self.assertEqual(output[0].text, "This is ")
        self.assertEqual(output[1].text_type, TextType.BOLD)
        self.assertEqual(output[1].text, "text")
        self.assertEqual(output[2].text_type, TextType.PLAIN)
        self.assertEqual(output[2].text, " with an ")
        self.assertEqual(output[3].text_type, TextType.ITALIC)
        self.assertEqual(output[3].text, "italic")
        self.assertEqual(output[4].text_type, TextType.PLAIN)
        self.assertEqual(output[4].text, " word and a ")
        self.assertEqual(output[5].text_type, TextType.CODE)
        self.assertEqual(output[5].text, "code block")
        self.assertEqual(output[6].text_type, TextType.PLAIN)
        self.assertEqual(output[6].text, " and an ")
        self.assertEqual(output[7].text_type, TextType.IMAGE)
        self.assertEqual(output[7].text, "obi wan image")
        self.assertEqual(output[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(output[8].text_type, TextType.PLAIN)
        self.assertEqual(output[8].text, " and a ")
        self.assertEqual(output[9].text_type, TextType.LINK)
        self.assertEqual(output[9].text, "link")
        self.assertEqual(output[9].url, "https://boot.dev")
        self.assertEqual(output[10].text_type, TextType.PLAIN)
        self.assertEqual(output[10].text, "")


if __name__ == "__main__":
    unittest.main()
