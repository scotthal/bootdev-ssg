import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """## heading _2_

### heading `3`"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>heading <i>2</i></h2><h3>heading <code>3</code></h3></div>"
        )

    def test_ordered_lists(self):
        md = """1. one
2. ordered
3. list

1. followed
2. _by_
3. another"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>ordered</li><li>list</li></ol><ol><li>followed</li><li><i>by</i></li><li>another</li></ol></div>"
        )

    def test_quotes(self):
        md = """> one
> quote

> followed
> `by`
> another"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>one quote</blockquote><blockquote>followed <code>by</code> another</blockquote></div>"
        )

    def test_unordered_lists(self):
        md = """- one
- ordered
- list

- followed
- _by_
- another"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>ordered</li><li>list</li></ul><ul><li>followed</li><li><i>by</i></li><li>another</li></ul></div>"
        )
