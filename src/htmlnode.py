class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        href = self.props["href"]
        target = self.props["target"]
        return f'href="{href}" target="{target}"'

    def __repr__(self):
        print(f"HTMLNode __repr__:\ntag={self.tag}\nvalue={self.value}\nchildren={self.children}\nprops={self.props}")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("value not found")
        elif not self.tag:
            return self.value
        else:
            if self.tag == "a":
                if not self.props:
                    raise ValueError("props not found")
                return f"""<a href="{self.props['href']}">{self.value}</a>"""
            elif self.tag == "img":
                if not self.props:
                    raise ValueError("props not found")
                src = self.props.get("src", "")
                alt = self.value or ""
                return f'<img src="{src}" alt="{alt}" />'
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag not found")
        else:
            message = str()
            for child in self.children:
                message += child.to_html()
            return f'<{self.tag}>{message}</{self.tag}>'

