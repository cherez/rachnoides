from rachnoides.renderer import *
from rachnoides.server import *

class Index(Node):
    async def render(self):
        title('test')
        center('Welcome to test site')
        hr()


server = Server(Index)
server.run()
