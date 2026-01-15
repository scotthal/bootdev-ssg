from ssgfiles import recursive_copy, recursive_delete
from textnode import TextNode, TextType


def main():
    print(TextNode("Howdy!", TextType.PLAIN, None))
    recursive_delete("public")
    recursive_copy("static", "public")


if __name__ == "__main__":
    main()
