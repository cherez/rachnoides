import xml.etree.ElementTree as ET

from .local import Local
from typing import List

tags = ['body', 'center', 'div', 'hr', 'p', 'br']


class Renderer:
    _element_stack: List[ET.Element]
    _context_stack: List
    context = ''
    content_element = None

    def path(self, obj):
        from .server import Node
        if isinstance(obj, str):
            return obj
        if issubclass(obj, Node):
            obj = obj()
        if isinstance(obj, Node):
            contexts = list(self._context_stack)
            while contexts:
                context = contexts[-1]
                if obj.__class__ in context.content:
                    break
                contexts.pop()
            if not contexts:
                raise ValueError()
            contexts.append(obj)
            return ''.join(i.path for i in contexts)

    class Element:
        def __init_subclass__(cls, **kwargs):
            cls.name = kwargs.get('name', cls.__name__)

        def __init__(self, text='', **kwargs):
            self.parent = self.renderer._element_stack[-1]
            if 'cls' in kwargs:
                kwargs['class'] = kwargs.pop('cls')
            self.element = ET.SubElement(self.parent, self.name)
            self.element.text = text
            self.element.attrib.update(kwargs)

        def __enter__(self):
            self.renderer._element_stack.append(self.element)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.renderer._element_stack.remove(self.element)

    class a(Element, name='a'):
        def __init__(self, href, text=''):
            super().__init__(text, href=self.renderer.path(href))

    def __init__(self):
        self.Element.renderer = self
        self.clear()

        for tag in tags:
            class TagElement(self.Element, name=tag):
                pass

            setattr(self, tag, TagElement)

    def clear(self):
        self.root = ET.Element('html')
        self.header = ET.SubElement(self.root, 'head')
        self.title_element = ET.SubElement(self.header, 'title')
        self.body_tag = ET.SubElement(self.root, 'body')
        self._element_stack = [self.root, self.body_tag]

    def render(self):
        return ET.tostring(self.root, 'unicode', 'xml', short_empty_elements=True)

    def title(self, text):
        self.title_element.text = text

    def content(self):
        self.content_element = self.div(id="content_" + self.context)

    def css(self, body):
        element = ET.SubElement(self.header, 'style')
        element.attrib['type'] = 'text/css'
        element.text = body


local = Local()


def wrap_method(name):
    def inner(*args, **kwargs):
        func = getattr(local.renderer, name)
        return func(*args, **kwargs)

    inner.name = name
    return inner


default_renderer = Renderer()
for tag in tags:
    globals()[tag] = wrap_method(tag)

a = wrap_method('a')
content = wrap_method('content')
css = wrap_method('css')
render = wrap_method('render')
title = wrap_method('title')


def clear():
    local.renderer = Renderer()
