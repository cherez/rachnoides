import xml.etree.ElementTree as ET

from typing import List

tags = ['body']

class Renderer:
    _stack: List[ET.Element]

    class Element:
        def __init_subclass__(cls, **kwargs):
            cls.name = kwargs.get('name', cls.__name__)

        def __init__(self):
            self.parent = self.renderer._stack[-1]
            self.element = ET.SubElement(self.parent, self.name)

        def __enter__(self):
            self.renderer._stack.append(self.element)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.renderer._stack.remove(self.element)

    def __init__(self):
        self.root = ET.Element('html')
        self.header = ET.SubElement(self.root, 'head')
        ET.SubElement(self.header, 'title')
        self._stack = [self.root]
        self.Element.renderer = self

        for tag in tags:
            class TagElement(self.Element, name=tag):
                pass
            setattr(self, tag, TagElement)

    def clear(self):
        self.root = ET.Element('html')
        self._stack = [self.root]

    def render(self):
        return ET.tostring(self.root, 'unicode', 'html')

    def title(self, text):
        self.header.find('title').text = text

default_renderer = Renderer()

