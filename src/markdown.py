import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        return []
    new_nodes = []
    for node in old_nodes:
        in_span = False
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            in_span = True
            continue

        splits = node.text.split(delimiter)
        for split in splits:
            if in_span:
                new_nodes.append(TextNode(split, text_type, node.url))
            else:
                new_nodes.append(TextNode(split, TextType.PLAIN, node.url))
            in_span = not in_span
    if not in_span:
        raise ValueError(f"Unbalanced delimier {delimiter}: {node.text}")
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
