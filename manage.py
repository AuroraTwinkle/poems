import tornado.ioloop
import tornado.web
from app.main.Poems import Poems
from app.main.User import User


class SelectPoemsHandler(tornado.web.RequestHandler):
    poems = Poems()

    def get(self):
        self.set_header('content-type', 'application/json')
        poems_index = int(self.get_argument("poems_index"))
        self.write(self.poems.getPoems(poems_index))


class RegisterUserHandler(tornado.web.RequestHandler):
    user = User()

    def get(self):
        user_mail = self.get_argument('user_mail')
        if self.user.searchMail(user_mail):
            self.write("True")
        else:
            self.write("False")

    def post(self):
        user_mail = self.get_argument('user_mail')
        user_password = self.get_argument('user_password')
        info_json = {"Name": "青莲居士", 'Ban': 0, 'id': user_mail, 'ReportNum': 0, 'Password': user_password,
                     'Banned': None, 'Photo': None, 'VoiceNum': 0, 'FavoritesNum': 0, 'EssayNum': 0, 'PoetryNum': 0,
                     'Vip': 0, 'VipTime': None}
        if self.user.registerUser(info_json):
            self.write("True")
        else:
            self.write("False")


def make_app():
    return tornado.web.Application([
        (r"/poems", SelectPoemsHandler),
        (r"/register", RegisterUserHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
