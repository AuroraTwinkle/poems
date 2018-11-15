from PTConnectionPool import PTConnectionPool, getPTConnection
import json


class User:
    def registerUser(self, info_json):
        status_code = self.searchMail(info_json["id"])
        status_code = json.loads(status_code)
        if status_code["status"]:
            return json.dumps({"status": False, "message": "Fail to register,The mail has existed!"},
                              ensure_ascii=False)
        sql = "insert into user (Name,Ban,id,ReportNum,Password,BanTime,Banned,Photo,VoiceNum,FavoritesNum,EssayNum,PoetryNum,Vip,VipTime) " \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  info_json["Name"], info_json["Ban"], info_json["id"],
                  info_json["ReportNum"], info_json["Password"], info_json["BanTime"],
                  info_json["Banned"], info_json["Photo"], info_json["VoiceNum"],
                  info_json["FavoritesNum"], info_json["EssayNum"], info_json["PoetryNum"],
                  info_json["Vip"], info_json["VipTime"])
        with getPTConnection() as db:
            if db.cursor.execute(sql):
                return json.dumps({"status": True, "message": "Register Successful!"}, ensure_ascii=False)
            else:
                return json.dumps({"status": False, "message": "Register Failed!"}, ensure_ascii=False)

    def searchMail(self, mail_id):
        sql = """select * from user where user.id='%s'""" % mail_id
        with getPTConnection() as db:
            if db.cursor.execute(sql):
                return json.dumps({"status": True, "message": "The mail has existed!"}, ensure_ascii=False)
            else:
                return json.dumps({"status": False, "message": "The mail has not existed!"}, ensure_ascii=False)

    def alterProfile(self, mail_id, user_name, user_avatar):
        status_code = self.searchMail(mail_id)
        status_code = json.loads(status_code)
        if not status_code["status"]:
            return json.dumps({"status": False, "message": "Fail to alter,The mail has not existed!"},
                              ensure_ascii=False)
        user_avatar = user_avatar.replace('\\', '/')
        sql = "update user set user.Name='%s',user.Photo='%s' where user.id='%s'" % (user_name, user_avatar, mail_id)
        with getPTConnection() as db:
            if db.cursor.execute(sql):
                return json.dumps({"status": True, "message": "Alter Successful!"}, ensure_ascii=False)
            else:
                return json.dumps({"status": False, "message": "Alter Failed!"}, ensure_ascii=False)

    def getProfile(self, mail_id):
        status_code = self.searchMail(mail_id)
        status_code = json.loads(status_code)
        if not status_code["status"]:
            return json.dumps({"status": False, "message": "Fail to get profile,The mail has not existed!"},
                              ensure_ascii=False)
        sql = "select Name,Photo from user where user.id='%s'" % mail_id
        with getPTConnection() as db:
            db.cursor.execute(sql)
            profile = db.cursor.fetchone()
            user_info = {'user_name': profile[0]}
            avatar_path = profile[1].replace('/', '\\')
            user_info['user_avatar'] = avatar_path
            user_info['status'] = True
            return json.dumps(user_info, ensure_ascii=False)
