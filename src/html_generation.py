from markdown_to_html import markdown_to_html_node


def extract_title(root_node):
    return root_node.children[0].children[0].value


def generate_html_document(html_template, markdown):
    root_node = markdown_to_html_node(markdown)
    title = extract_title(root_node)
    result = html_template.replace("{{ Title }}", title)
    result = result.replace("{{ Content }}", root_node.to_html())
    return result
