import unittest

from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("h1", "value", ["a", "b", "c"], {"href": "https://www.google.com", "target": "_blank"})
        assert node.props_to_html() == 'href="https://www.google.com" target="_blank"'

    def test_None(self):
        node = HTMLNode()
        assert (node.tag == None and node.value == None and node.children == None and node.props == None)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_error(self):
        node = LeafNode(None, "i dont love you like i did yesterday")
        self.assertEqual(node.to_html(), "i dont love you like i did yesterday")

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children(self):
        child_node1 = LeafNode("p", "hello")
        child_node2 = LeafNode("p", "world")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>hello</p><p>world</p></div>"
        )

if __name__ == "__main__":
    unittest.main()
