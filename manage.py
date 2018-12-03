import tornado.ioloop
import tornado.web
from datetime import datetime
from app.main.Poems import Poems
from app.main.User import User


class LoginHandler(tornado.web.RequestHandler):
    user = User()

    def post(self):
        mail_id = self.get_argument('mail_id')
        password = self.get_argument('password')
        self.write(self.user.login(mail_id, password))


class SelectPoemsHandler(tornado.web.RequestHandler):
    poems = Poems()

    def get(self):
        self.set_header('content-type', 'application/json')
        poems_index = int(self.get_argument("poems_index"))
        self.write(self.poems.getPoems(poems_index))

    def post(self):
        poem_info = {}
        poem_info['Title'] = self.get_argument("poem_title")
        poem_info['Editor'] = self.get_argument("poem_editor")
        poem_info['Uploader'] = self.get_argument("poem_uploader")
        poem_info['Dynasty'] = self.get_argument("poem_dynasty")
        poem_info['Note'] = ''
        poem_info['ReportNum'] = 0
        poem_info['Translate'] = ''
        poem_info['shangxi'] = ''
        poem_info['LikeTotal'] = 0
        poem_files = self.request.files['poem']
        for poem in poem_files:
            file_name = poem['filename']
            import os
            if not os.path.exists('C:\古诗词\诗歌内容'):
                os.makedirs('C:\古诗词\诗歌内容')
            import uuid
            uuid_str = uuid.uuid1()
            poem_path = ('''C:\古诗词\诗歌内容\\''' + '%s' + file_name) % uuid_str
            with open(poem_path, 'wb') as up:
                up.write(poem['body'])
            poem_info['Path'] = poem_path
            self.write(self.poems.addPoem(poem_info))


class RegisterUserHandler(tornado.web.RequestHandler):
    user = User()

    def get(self):
        user_mail = self.get_argument('user_mail')
        self.write(self.user.searchMail(user_mail))

    def post(self):
        user_mail = self.get_argument('user_mail')
        user_password = self.get_argument('user_password')
        now_time = datetime.now()
        info_json = {'Name': "青莲居士", 'Ban': 0, 'id': user_mail, 'ReportNum': 0, 'Password': user_password,
                     'BanTime': now_time,
                     'Banned': None, 'Photo': None, 'VoiceNum': 0, 'FavoritesNum': 0, 'EssayNum': 0, 'PoetryNum': 0,
                     'Vip': 0, 'VipTime': now_time}
        self.write(self.user.registerUser(info_json))


class AlterProfileHandler(tornado.web.RequestHandler):
    user = User()

    def get(self):
        user_mail = self.get_argument('user_mail')
        user_info = self.user.getProfile(user_mail)
        self.write(user_info)

    def post(self):
        user_mail = self.get_argument('user_mail')
        user_name = self.get_argument('user_name')
        avatar_info = self.request.files['user_avatar']
        for avatar in avatar_info:
            file_name = avatar['filename']
            import os
            if not os.path.exists('C:\古诗词\用户头像'):
                os.makedirs('C:\古诗词\用户头像')
            import uuid
            uuid_str = uuid.uuid1()
            avatar_path = ('''C:\古诗词\用户头像\\''' + '%s' + file_name) % uuid_str
            with open(avatar_path, 'wb') as up:
                up.write(avatar['body'])
            self.write(self.user.alterProfile(user_mail, user_name, avatar_path))


class UploadPhotoHandler(tornado.web.RequestHandler):
    def get(self):
        avatar_path = self.get_argument('user_avatar')
        with open(avatar_path, 'rb') as f:
            self.set_header("Content-Type", "image/jpg")
            self.write(f.read())


def make_app():
    return tornado.web.Application([
        (r"/poems", SelectPoemsHandler),
        (r"/register", RegisterUserHandler),
        (r"/alterOrGetProfile", AlterProfileHandler),
        (r"/getAvatar", UploadPhotoHandler),
        (r"/login", LoginHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
