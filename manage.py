import tornado.ioloop
import tornado.web
from Poems import Poems


class PoemsHandler(tornado.web.RequestHandler):
    poems = Poems()

    def get(self):
        poems_index = int(self.get_argument("poems_index"))
        self.write(self.poems.getPoems(poems_index))


def make_app():
    return tornado.web.Application([
        (r"/poems", PoemsHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
