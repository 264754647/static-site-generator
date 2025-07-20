import re

from textnode import *
from htmlnode import *
from blocktypes import *


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("not a textnode")
    else:
        if text_node.text_type == TextType.text:
            return LeafNode(None, text_node.text)

        elif text_node.text_type == TextType.bold:
            return LeafNode("b", text_node.text)

        elif text_node.text_type == TextType.italic:
            return LeafNode("i", text_node.text)

        elif text_node.text_type == TextType.code:
            return LeafNode("code", text_node.text)

        elif text_node.text_type == TextType.link:
            return LeafNode("a", text_node.text, text_node.url)

        elif text_node.text_type == TextType.image:
            return LeafNode("img", text_node.text, text_node.url)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = list()
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            result.append(old_node)
            continue
        if delimiter not in ["**", "_", "`"]:
            raise Exception("invalid delimiter")
        new_node = list()
        phrases = old_node.text.split(delimiter)
        for phrase in phrases:
            if not phrase:
                continue
            if phrases.index(phrase) % 2 == 0:
                new_node.append(TextNode(phrase, old_node.text_type))
            else:
                new_node.append(TextNode(phrase, text_type))
        result.extend(new_node)
    return result

def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)

def split_nodes_image(old_nodes):
    result = list()
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            result.append(old_node)
            continue
        text_url_list = extract_markdown_images(old_node.text)
        if not text_url_list:
            result.append(TextNode(old_node.text, old_node.text_type))
        else:
            text = old_node.text
            for alt, url in text_url_list:
                parts = text.split(f"![{alt}]({url})", 1)
                if parts[0]:
                    result.append(TextNode(parts[0], old_node.text_type))
                result.append(TextNode(alt, TextType.image, {"src": url}))
                text = parts[1]
            if text:
                result.append(TextNode(text, old_node.text_type))
    return result

def split_nodes_link(old_nodes):
    result = list()
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            result.append(old_node)
            continue
        text_url_list = extract_markdown_links(old_node.text)
        if not text_url_list:
            result.append(TextNode(old_node.text, old_node.text_type))
        else:
            text = old_node.text
            for alt, url in text_url_list:
                parts = text.split(f"[{alt}]({url})", 1)
                if parts[0]:
                    result.append(TextNode(parts[0], old_node.text_type))
                result.append(TextNode(alt, TextType.link, {"href": url}))
                text = parts[1]
            if text:
                result.append(TextNode(text, old_node.text_type))
    return result

def text_to_textnodes(text):
    node = [TextNode(text, TextType.text)]
    node = split_nodes_delimiter(node, "**", TextType.bold)
    node = split_nodes_delimiter(node, "_", TextType.italic)
    node = split_nodes_delimiter(node, "`", TextType.code)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    list_blocks = list()
    for block in blocks:
        block = block.strip()
        lines = block.split("\n")
        list_lines = list()
        for line in lines:
            line = line.strip()
            if line:
                list_lines.append(line)
        new_block = "\n".join(list_lines)
        list_blocks.append(new_block)
    return list_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    pattern = re.compile(r'^\s*\d+\.\s')
    if not block:
        return BlockType.paragraph
    if re.match(r'#{1,6} ', block):
        return BlockType.heading
    if block.startswith("`") and block.endswith("`"):
        return BlockType.code
    if all(line.startswith(">") for line in lines if line.strip()):
        return BlockType.quote
    if all(line.startswith("- ") for line in lines if line.strip()):
        return BlockType.unordered_list
    if all(pattern.match(line) for line in lines if line.strip()):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    final_list = list()
    for text_node in text_nodes:
        split_node = text_node_to_html_node(text_node)
        final_list.append(split_node)
    return final_list

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_children = list()
    for block in blocks:
        if not block:
            continue
        type = block_to_block_type(block)
        if type == BlockType.heading:
            count = block.split()[0].count("#")
            text = block[count+1:].strip()
            children = text_to_children(text)
            node = ParentNode(tag=f"h{count}", children=children)
        elif type == BlockType.code:
            text = block.strip("`")
            text = text.lstrip("\n")
            node = ParentNode(tag="pre", children=[
                ParentNode(tag="code", children=[LeafNode(tag=None, value=text)]
            )])
        elif type == BlockType.quote:
            lines = block.split("\n")
            texts = list()
            for line in lines:
                text = line.lstrip("> ").strip()
                texts.append(text)
            quote = " ".join(texts)
            children = text_to_children(quote)
            node = ParentNode(tag="blockquote", children=children)
        elif type == BlockType.unordered_list:
            lines = block.split("\n")
            list_lines = list()
            for line in lines:
                text = line[2:].strip()
                children = text_to_children(text)
                list_lines.append(ParentNode(tag="li", children=children))
            node = ParentNode(tag="ul", children=list_lines)
        elif type == BlockType.ordered_list:
            lines = block.split("\n")
            list_lines = list()
            for line in lines:
                text = line[3:].strip()
                children = text_to_children(text)
                list_lines.append(ParentNode(tag="li", children=children))
            node = ParentNode(tag="ol", children=list_lines)
        elif type == BlockType.paragraph:
            text = block.strip()
            text = text.replace("\n", " ")
            children = text_to_children(text)
            node = ParentNode(tag="p", children=children)
        else:
            raise ValueError("invalid type")

        div_children.append(node)
    return ParentNode(tag="div", children=div_children)

def extract_title(markdown):
    match = re.match(r'#{1,6} ', markdown)
    if not match:
        raise Exception("no title found")
    else:
        stripped = markdown.lstrip(match.group(0)).strip()
        return stripped
