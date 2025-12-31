from htmlnode import HTMLNode


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
