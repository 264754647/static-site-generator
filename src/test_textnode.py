import unittest

from textnode import *
from htmlnode import *
from functions import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node1, node2)

    def test_url(self):
        node1 = TextNode("This is a text node", TextType.bold, "url")
        assert node1.url

    def test_text(self):
        node1 = TextNode("a", TextType.bold)
        node2 = TextNode("b", TextType.italic)
        assert (node1.text != node2.text), (node1.text_type != node2.text_type)

if __name__ == "__main__":
    unittest.main()
