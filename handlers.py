#!/usr/bin/python3
import tornado.web
import json
from tornado.escape import json_decode
from tornado.escape import json_encode
import sqlite3
import datetime
import settings


db = sqlite3.connect(settings.DB_NAME)


async def get_query(sql):
    with open(sql, 'r') as f:
        query = ''.join(f.readlines())
    return query


class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        self.render("index.html", messages=None)


class AjaxHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ('GET', 'POST', 'DELETE')

    async def delete(self):
        print('REST.delete data received:', self.request.body)
        json_data = json_decode(self.request.body)
        print('REST.delete json data received:', json_data)
        query = await get_query('sql/delete_rows.sql')
        response = {'method': 'delete'}
        try:
            c = db.cursor()
            for r in json_data['delete']:
                c.execute(query, {'id': r, })
            c.close()
            db.commit()
            response.update({
                             'code': 0,
                             'deleted': len(json_data['delete'])
                            })
        except Exception as e:
            db.rollback()
            response.update({'code': -1, 'error': str(e)})
        print(response)
        self.write(json_encode(response))

    async def get(self):
        print('REST.get data received:', self.request.body)
        # json_data = json_decode(self.request.body)
        # print('REST.get json data received:', json_data)
        query = await get_query('sql/select_rows.sql')
        response = {'method': 'get'}
        try:
            c = db.cursor()
            print(query)
            response.update({
                        'code': 0,
                        'result': {r[0]: r[1] for r in c.execute(query)},
                       })
            c.close()
        except Exception as e:
            response.update({'code': -1, 'result': str(e), })
        print('REST.get data response:', response)
        self.write(json_encode(response))

    async def post(self):
        json_data = json_decode(self.request.body)
        print('REST.post json data received', json_data)
        query = await get_query('sql/insert_row.sql')
        response = {'method': 'post', }
        try:
            c = db.cursor()
            c.execute(query, {'TEXT': json_data['txt'], })
            response.update({
                        'code': 0,
                        'id': c.lastrowid,
                       })
            c.close()
            db.commit()
        except Exception as e:
            db.rollback()
            response.update({'code': -1, 'error': str(e)})

        self.write(json_encode(response))
