import unittest

from textnode import *
from functions import *

class TestFunctions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")

    def test_link(self):
        node = TextNode("This is a text node", TextType.link, "url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, "url")

    def test_image(self):
        node = TextNode("This is a text node", TextType.image, "url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")

    def test_basic_split_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        expected = [
            TextNode("This is text with a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" word", TextType.text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_split_delimiter(self):
        node1 = TextNode("the message is in **bold** hopefully", TextType.text)
        node2 = TextNode("an _italic_ text", TextType.text)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.italic)
        expected = [
            TextNode("the message is in **bold** hopefully", TextType.text),
            TextNode("an ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" text", TextType.text),
        ]
        self.assertEqual(new_nodes, expected)

    def test_whole_split_delimiter(self):
        node = TextNode("**THIS IS NOT A DRILL**", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        expected = [
            TextNode("THIS IS NOT A DRILL", TextType.bold),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images_1(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text),
                TextNode("second image", TextType.image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_2(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.text),
                TextNode("second image", TextType.image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_3(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_4(self):
        node1 = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text,
        )
        node2 = TextNode(
            "![image](https://i.imgur.com/3elNhQu.png)",
            TextType.text,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("image", TextType.image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.image, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_1(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.google.com)",
            TextType.text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("link", TextType.link, "https://www.boot.dev"),
                TextNode(" and another ", TextType.text),
                TextNode("second link", TextType.link, "https://www.google.com"),
            ],
            new_nodes,
        )


    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.text),
                TextNode("text", TextType.bold),
                TextNode(" with an ", TextType.text),
                TextNode("italic", TextType.italic),
                TextNode(" word and a ", TextType.text),
                TextNode("code block", TextType.code),
                TextNode(" and an ", TextType.text),
                TextNode("obi wan image", TextType.image, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.text),
                TextNode("link", TextType.link, "https://boot.dev"),
            ],
            text_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.heading)
        self.assertEqual(block_to_block_type("###### Deep header"), BlockType.heading)
        self.assertNotEqual(block_to_block_type("####### Too many"), BlockType.heading)

    def test_code(self):
        self.assertEqual(block_to_block_type("`inline code`"), BlockType.code)
        self.assertNotEqual(block_to_block_type("`not closed"), BlockType.code)
        self.assertNotEqual(block_to_block_type("code without backticks"), BlockType.code)

    def test_quote(self):
        quote_block = "> Quote line\n> Another quote"
        self.assertEqual(block_to_block_type(quote_block), BlockType.quote)
        non_quote_block = "> Quote line\nNo quote here"
        self.assertNotEqual(block_to_block_type(non_quote_block), BlockType.quote)

    def test_unordered_list(self):
        ul_block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul_block), BlockType.unordered_list)
        mixed_block = "- Item 1\nNot an item"
        self.assertNotEqual(block_to_block_type(mixed_block), BlockType.unordered_list)

    def test_ordered_list(self):
        ol_block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ordered_list)
        mixed_block = "1. Item 1\nItem 2"
        self.assertNotEqual(block_to_block_type(mixed_block), BlockType.ordered_list)

    def test_paragraph(self):
        para = "Just a normal paragraph without any special formatting."
        self.assertEqual(block_to_block_type(para), BlockType.paragraph)
        self.assertEqual(block_to_block_type(""), BlockType.paragraph)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blankline(self):
        md = """
    # Heading One

    This is a paragraph with **bold** and _italic_ text.

    ## Heading Two
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading One</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><h2>Heading Two</h2></div>",
        )

    def test_extra_space(self):
        self.assertEqual(extract_title("##     Extra space"), "Extra space")

    def test_not_a_heading(self):
        with self.assertRaises(Exception) as context:
            extract_title("No heading here")
        self.assertEqual(str(context.exception), "no title found")

if __name__ == "__main__":
    unittest.main()
