from aiohttp import web
from renderer import *


class Node:
    default_content = None
    content = []

    def render(self):
        pass


class Server:
    def __init__(self, root):
        self.app = web.Application()
        self.root = root
        self.app.router.add_route('*', '/{tail:.*}', self.handle)

    async def handle(self, request):
        parts = request.path.split('/')
        parts = [i for i in parts if i]  # remove blanks
        print(parts)
        default_renderer.context = 'root'
        clear()
        top = default_renderer.root
        node = self.root()
        node.render()
        while default_renderer.content:
            content = default_renderer.content_element
            if not node.default_content:
                break
            node = node.default_content()
            default_renderer.content_element = None
            with content:
                node.render()

        return web.Response(text=render(), content_type='text/html')

    def run(self, host='127.0.0.1', port=8080):
        web.run_app(self.app, host=host, port=port)


class Index(Node):
    def render(self):
        p('Welcome to test site')
        hr()
        with div(cls='section'):
            for i in range(30):
                with div(cls='small-box'):
                    a('/link', 'Module name')
                    br()
                    p('Long description of what this module does')


class Root(Node):
    default_content = Index
    css = open('test.css').read()
    def render(self):
        title('test title')
        css(self.css)
        with body():
            p('hello world')
            content()


Server(Root).run()
