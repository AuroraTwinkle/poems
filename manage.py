import tornado.ioloop
import tornado.web
from poems import Poems


class PoemsHandler(tornado.web.RequestHandler):
    poems = Poems()

    def get(self):
        sum = int(self.get_argument("poems_sum"))
        self.write(self.poems.getPoems(sum))


def make_app():
    return tornado.web.Application([
        (r"/", PoemsHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
