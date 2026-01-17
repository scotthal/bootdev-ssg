from html_generation import generate_html_document
from ssgfiles import recursive_copy, recursive_delete


def main():
    recursive_delete("public")
    recursive_copy("static", "public")
    with open("content/index.md", encoding="utf-8") as input_file:
        markdown = input_file.read()
    with open("template.html", encoding="utf-8") as template_file:
        html_template = template_file.read()
    print("Generate document public/index.html from input content/index.md")
    html_document = generate_html_document(html_template, markdown)
    with open("public/index.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_document)


if __name__ == "__main__":
    main()
