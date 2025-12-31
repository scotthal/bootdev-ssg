import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode(None, "howdy")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("body", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html())

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", {"class": "x"}),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text", {"class": "y"}),
                LeafNode(None, "Normal text"),
            ],
            {"class": "fake"},
        )
        self.assertEqual(
            "<p class=\"fake\"><b class=\"x\">Bold text</b>Normal text<i class=\"y\">italic text</i>Normal text</p>",
            node.to_html())

    def test_to_html_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node], {"class": "fake"})
        parent_node = ParentNode("div", [child_node], {"class": "elite"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"elite\"><span class=\"fake\"><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
