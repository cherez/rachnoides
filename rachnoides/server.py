from asyncio import Task, sleep

from aiohttp import web
from .renderer import *


class Node:
    default_content = None
    content = []
    name = None

    async def render(self):
        pass

    def content_for(self, path):
        for c in self.content:
            if c.matches(path):
                return c(path)
        return None

    @classmethod
    def matches(cls, path):
        return (cls.name or cls.__name__).lower() == path.lower()

    def __init_subclass__(cls, **kwargs):
        cls.path = (cls.__name__ or cls.__name__).lower() + '/'

    def __init__(self, path=None):
        pass


class Server:
    def __init__(self, root):
        self.app = web.Application()
        self.root = root
        root.name = ''
        root.path = '/'
        self.app.router.add_route('*', '/{tail:.*}', self.handle)

    async def handle(self, request):
        parts = request.path.split('/')
        parts = [i for i in parts if i]  # remove blanks
        clear()
        renderer = local.renderer
        renderer.context = 'root'
        node = self.root()
        renderer._context_stack = [node]
        await node.render()
        while renderer.content:
            content_tag = renderer.content_element
            if parts:
                part = parts.pop(0)
                node = node.content_for(part)
                if not node:
                    # TODO: 404
                    break
            elif node.default_content:
                node = node.default_content()
            else:
                break
            renderer.content_element = None
            renderer._context_stack.append(node)
            with content_tag:
                await node.render()

        return web.Response(text=render(), content_type='text/html')

    def run(self, host='127.0.0.1', port=8080):
        web.run_app(self.app, host=host, port=port)

    async def attach(self, loop, host='127.0.0.1', port=8080):
        await self.app.startup()
        handler = self.app.make_handler(loop=loop)
        await loop.create_server(handler, host, port)
