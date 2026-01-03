import re

from textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    return [l.strip() for l in markdown.split("\n\n") if l != ""]


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


IMAGE_PATTERN = r"!\[(.*?)\]\((.*?)\)"


def extract_markdown_images(text):
    return re.findall(IMAGE_PATTERN, text)


LINK_PATTERN = r"(?<!!)\[(.*?)\]\((.*?)\)"


def extract_markdown_links(text):
    return re.findall(LINK_PATTERN, text)


def split_nodes_pattern(old_nodes, pattern, text_type):
    if len(old_nodes) == 0:
        return []
    new_nodes = []
    for node in old_nodes:
        current_start = 0
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        for match in re.finditer(pattern, node.text):
            start = match.start()
            end = match.end()
            new_nodes.append(
                TextNode(node.text[current_start:start], TextType.PLAIN))
            link_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(link_text, text_type, url))
            current_start = end
        new_nodes.append(TextNode(node.text[current_start:], TextType.PLAIN))
    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_pattern(old_nodes, IMAGE_PATTERN, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes_pattern(old_nodes, LINK_PATTERN, TextType.LINK)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)
