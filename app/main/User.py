from PTConnectionPool import PTConnectionPool, getPTConnection


class User:
    def registerUser(self, info_json):
        sql = "insert into user (Name,Ban,id,ReportNum,Password,BanTime,Banned,Photo,VoiceNum,FavoritesNum,EssayNum,PoetryNum,Vip,VipTime) " \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  info_json["Name"], info_json["Ban"], info_json["id"],
                  info_json["ReportNum"], info_json["Password"], info_json["BanTime"],
                  info_json["Banned"], info_json["Photo"], info_json["VoiceNum"],
                  info_json["FavoritesNum"], info_json["EssayNum"], info_json["PoetryNum"],
                  info_json["Vip"], info_json["VipTime"])
        with getPTConnection() as db:
            return db.cursor.execute(sql)

    def searchMail(self, mail_id):
        sql = "select * from user where user.id=%s" % mail_id
        with getPTConnection() as db:
            return db.cursor.execute(sql)

    def alterProfile(self, mail_id, user_name, user_avatar):
        if not self.searchMail(mail_id):
            return False
        sql = "update user set user.Name=%s,user.Photo=%s where user.id=%s" % (user_name, user_avatar, mail_id)
        with getPTConnection() as db:
            return db.cursor.execute(sql)
