from markdown import BlockType, heading_block_level

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes must override")

    def props_to_html(self):
        result = ""
        first = True
        for prop in self.props:
            if first:
                first = False
            else:
                result += " "
            result += f"{prop}=\"{self.props[prop]}\""
        return result

    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

def html_node_from_block_type(block_type, block):
    match block_type:
        case BlockType.CODE:
            return HTMLNode("pre", None, HTMLNode("code"))
        case BlockType.HEADING:
            return HTMLNode(f"h{heading_block_level(block)}")
        case BlockType.ORDERED_LIST:
            return HTMLNode("ol")
        case BlockType.PARAGRAPH:
            return HTMLNode("p")
        case BlockType.QUOTE:
            return HTMLNode("blockquote")
        case BlockType.UNORDERED_LIST:
            return HTMLNode("ul")
        case _:
            raise ValueError(f"Unknown block type {block_type}")
