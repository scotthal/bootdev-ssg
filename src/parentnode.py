from htmlnode import HTMLNode

from markdown import BlockType, heading_block_level


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")

        if self.children is None:
            raise ValueError("ParentNode requires children")

        if self.props is None:
            result = f"<{self.tag}>"
        else:
            result = f"<{self.tag} {self.props_to_html()}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"
        return result


def parent_node_from_block_type(block_type, block):
    match block_type:
        case BlockType.CODE:
            return ParentNode("pre", [])
        case BlockType.HEADING:
            return ParentNode(f"h{heading_block_level(block)}", [])
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", [])
        case BlockType.PARAGRAPH:
            return ParentNode("p", [])
        case BlockType.QUOTE:
            return ParentNode("blockquote", [])
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", [])
        case _:
            raise ValueError(f"Unknown block type {block_type}")
