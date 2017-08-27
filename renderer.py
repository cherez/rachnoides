import xml.etree.ElementTree as ET

from typing import List

tags = ['body', 'div', 'hr', 'p', 'br']

class Renderer:
    _stack: List[ET.Element]
    context = ''
    content_element = None

    class Element:
        def __init_subclass__(cls, **kwargs):
            cls.name = kwargs.get('name', cls.__name__)

        def __init__(self, text='', **kwargs):
            self.parent = self.renderer._stack[-1]
            if 'cls' in kwargs:
                kwargs['class'] = kwargs.pop('cls')
            self.element = ET.SubElement(self.parent, self.name)
            self.element.text = text
            self.element.attrib.update(kwargs)

        def __enter__(self):
            self.renderer._stack.append(self.element)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.renderer._stack.remove(self.element)

    class a(Element, name='a'):
        def __init__(self, href, text):
            super().__init__(text, href=href)

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
        return ET.tostring(self.root, 'unicode', 'xml', short_empty_elements=True)

    def title(self, text):
        self.header.find('title').text = text

    def content(self):
        self.content_element = self.div(id="content_" + self.context)

    def css(self, body):
        element = ET.SubElement(self.root, 'style')
        element.attrib['type'] = 'text/css'
        element.text = body

default_renderer = Renderer()
for tag in tags:
    globals()[tag] = getattr(default_renderer, tag)
render = default_renderer.render
title = default_renderer.title
clear = default_renderer.clear
a = default_renderer.a
content = default_renderer.content
css = default_renderer.css