import json
from PTConnectionPool import getPTConnection
import datetime
import random


class Poems:
    dateTimeDay = datetime.datetime.now().day

    def getPoems(self, poems_index=1):

        with getPTConnection() as db:
            poetry_totals = db.cursor.execute('select * from poetry')
            if datetime.datetime.now().day - self.dateTimeDay >= 1:
                self.dateTimeDay = datetime.datetime.now().day
                baseIndex = random.randint(1, poetry_totals // 10)
                poems_index += baseIndex
            if 10 * poems_index > poetry_totals or poems_index < 1:
                poems_index = 1

            sql = 'select * from poetry limit ' + str((poems_index - 1) * 10) + ',' + str(10)
            db.cursor.execute(sql)
            poems = self.changeJson(db.cursor.fetchall())
        return poems

    def changeJson(self, data):
        jsonDt = []
        for row in data:
            result = {}
            result['Title'] = row[0]
            if row[1] != '':
                with open(row[1], 'r', encoding='UTF-8') as f:
                    note = f.read()
                    result['Note'] = note

            result['Editor'] = row[2]
            if row[3] != '':
                with open(row[3], 'r', encoding='UTF-8') as f:
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
            jsonDt.append(result)
        return json.dumps(jsonDt, ensure_ascii=False)
