from renderer import *
class Index(Node):
    def render(self):
        center('Welcome to test site')
        hr()
        with div(flex_flow='row'):
            for module in modules:
                with div(flex='1 1'):
                    link(Root / module.Root, module.name)
                    br()
                    text(module.description)


class Root(Node):
    content = [Index] + [i.Root for i in modules]
    def render(self):
        title('test title')
        body(
            content(default=Index)
        )