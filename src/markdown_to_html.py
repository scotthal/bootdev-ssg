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
        case BlockType.HEADING:
            return heading_to_children(text)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_children(text)
        case BlockType.PARAGRAPH:
            return leaf_children(text)
        case BlockType.QUOTE:
            return quote_to_children(text)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_children(text)
        case _:
            raise NotImplementedError()


def heading_to_children(text):
    i = 0
    while i < len(text):
        if text[i] != "#":
            break
        i += 1
    return leaf_children(text[i:].strip())


def ordered_list_to_children(text):
    children = []
    lines = text.splitlines()
    i = 1
    for line in lines:
        digits = len(str(i))
        children.append(
            ParentNode("li", leaf_children(line[digits + 2:].strip())))
        i += 1
    return children


def leaf_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def quote_to_children(text):
    children = []
    lines = text.splitlines()
    first = True
    for line in lines:
        actual_line = line[1:].strip()
        if not first:
            actual_line = " " + actual_line
        children.extend(leaf_children(actual_line))
        first = False
    return children


def unordered_list_to_children(text):
    children = []
    lines = text.splitlines()
    for line in lines:
        children.append(ParentNode("li", leaf_children(line[2:].strip())))
    return children
