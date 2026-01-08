from leafnode import text_node_to_html_node
from markdown import BlockType, block_to_block_type, markdown_to_blocks
from markdown import text_to_textnodes
from parentnode import ParentNode, parent_node_from_block_type


def markdown_to_html_node(markdown):
    root_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        parent_node = parent_node_from_block_type(block_type, block)
        parent_node.children = text_to_children(block_type, block)
        root_node.children.append(parent_node)
    return root_node


def text_to_children(block_type, text):
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_children(text)
        case _:
            raise NotImplementedError()


def paragraph_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]
