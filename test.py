from rachnoides.renderer import *
from rachnoides.server import *

class About(Node):
    async def render(self):
        h1('rachnoides lets you write HTML with python functions')
        br()
        with center():
            b('they can be nested using with blocks')
        br()
        for i in range(5):
            p('you can use normal Python control flow in these')
        a(Root, 'It also handles links pretty nicely')


class Index(Node):
    async def render(self):
        # set CSS class with cls, because reserved words
        with div(cls='section'):
            for node in Root.content:
                with a(node):
                    with div(cls='small-box'):
                        b(node.__name__)


class Root(Node):
    # a node can have 'content', which are child nodes that can be embedded in it
    # this node will be addressed at '/about'
    content = [About]
    # defaults to this node if none are specified; so '/' will embed Index
    default_content = Index

    css = open('test.css').read()

    async def render(self):
        # sets the page title; later calls override
        title('Test page')

        # embed CSS in the page
        css(self.css)

        # renders <center><h1>Welcome to test site</h1></center>
        with center():
            h1('Welcome to test site')
        # renders <center>The testest site</center>
        center('The testest site')
        # renders <hr/>
        hr()
        # content() is where child nodes render their content
        content()


# the Server class takes a root node for its argument
server = Server(Root)
# runs the server; this will start an asyncio event loop running the server
# you can specify address and port as well
server.run()
# you can also use attach() to insert the server in an existing event loop to embed in other programs
