import os
import shutil

from textnode import TextNode
from htmlnode import *
from functions import *


def static_to_public(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise Exception("source doesn't exist")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    contents = os.listdir(source_dir)
    for content in contents:
        path_source = os.path.join(source_dir, content)
        path_dest = os.path.join(dest_dir, content)
        if os.path.isfile(path_source):
            shutil.copy(path_source, path_dest)
        else:
            os.mkdir(path_dest)
            static_to_public(path_source, path_dest)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        from_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    html_string = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    content = template_content.replace("{{ Title }}", title)
    content = content.replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for content in contents:
        path = os.path.join(dir_path_content, content)
        if os.path.isfile(path):
            filename = os.path.splitext(content)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, filename)
            generate_page(path, template_path, dest_path)
        else:
            static_to_public(path, os.path.join(dest_dir_path, content))
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, content))

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
