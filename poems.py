import json
from PTConnectionPool import getPTConnection


class Poems():
    reque_count = 1

    def getPoems(self, sum=10):
        with getPTConnection() as db:
            poetry_totals = db.cursor.execute('select * from poetry')
            if self.reque_count * sum > poetry_totals:
                self.reque_count = 1

            sql = 'select * from poetry limit ' + str((self.reque_count - 1) * sum) + ',' + str(sum)
            db.cursor.execute(sql)
            poems = self.changeJson(db.cursor.fetchall())
            self.reque_count += 1
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
            result['ReportNum'] = row[4]
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
