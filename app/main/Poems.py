import json
from PTConnectionPool import getPTConnection
import datetime
import random

from app.main.User import User


class Poems:
    dateTimeDay = datetime.datetime.now().day

    def addPoem(self, info_json):
        user = User()
        status_code = user.searchMail(info_json["Uploader"])
        status_code = json.loads(status_code)
        if not status_code["status"]:
            return json.dumps({"status": False, "message": "Fail to add poem,The mail has not existed!"},
                              ensure_ascii=False)
        poem_path = info_json["Path"]
        poem_path = poem_path.replace('\\', '/')
        sql = "insert into poetry (Title,Note,Editor,Path,ReportNum,Uploader,Translate,Dynasty,shangxi,LikeTotal)" \
              "values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                  info_json["Title"], info_json["Note"], info_json["Editor"],
                  poem_path, info_json["ReportNum"], info_json["Uploader"],
                  info_json["Translate"], info_json["Dynasty"], info_json["shangxi"],
                  info_json["LikeTotal"])
        with getPTConnection() as db:
            if db.cursor.execute(sql):
                return json.dumps({"status": True, "message": "successful to upload poem!"}, ensure_ascii=False)
            else:
                return json.dumps({"status": False, "message": "fail to upload poem!"}, ensure_ascii=False)

    def getPoems(self, poems_index=1):

        with getPTConnection() as db:
            poetry_totals = db.cursor.execute('select * from poetry')
            if datetime.datetime.now().day - self.dateTimeDay >= 1:
                self.dateTimeDay = datetime.datetime.now().day
                base_index = random.randint(1, poetry_totals // 10)
                poems_index += base_index
            if 10 * poems_index > poetry_totals or poems_index < 1:
                poems_index = 1

            sql = 'select * from poetry limit ' + str((poems_index - 1) * 10) + ',' + str(10)
            db.cursor.execute(sql)
            poems = self.changeJson(db.cursor.fetchall())
        return poems

    def changeJson(self, data):
        json_dt = []
        for row in data:
            result = {'Title': row[0]}
            sql = "select Photo from user where id=%s" % row[5]
            with getPTConnection() as db:
                db.cursor.execute(sql)
                photo = db.cursor.fetchone()
                result['user_avatar'] = '0'
                if photo[0] != '':
                    result['user_avatar'] = photo[0].replace('/', '\\')


            if row[1] != '':
                with open(row[1], 'r', encoding='UTF-8') as f:
                    note = f.read()
                    result['Note'] = note

            result['Editor'] = row[2]
            if row[3] != '':
                path_poem = row[3]
                path_poem = path_poem.replace('/', '\\')
                with open(path_poem, 'r', encoding='UTF-8') as f:
                    poery = f.read()
                    result['Poetry'] = poery
            if row[6] != '':
                with open(row[6], 'r', encoding='UTF-8') as f:
                    translate = f.read()
                    result['Translate'] = translate

            result['Dynasty'] = row[7]
            if row[8] != '':
                with open(row[8], 'r', encoding='UTF-8') as f:
                    shangxi = f.read()
                    result['shangxi'] = shangxi

            result['LikeTotal'] = row[9]
            json_dt.append(result)
        return json.dumps(json_dt, ensure_ascii=False)
