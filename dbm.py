# -*- coding: utf-8 -*-
from pymongo import MongoClient
import datetime

class Connector_DBM:

    def __init__(self, host, port, user, password, db):
        __conn = MongoClient(host, port)
        self.__handle = __conn[db]
        self.__handle.authenticate(user, password)

    def insert_email(self, json, test):
        json['test'] = test
        json['datetime'] = datetime.datetime.now()
        id_row = self.__handle.ses.insert(json)
        return id_row

    def update_email(self, id_row, MessageId):

        self.__handle.ses.update_one({"_id": id_row}, {"$set": {"MessageId": MessageId}})

    def verify_app(self, token_app):
        try:
            return str(self.__handle.ses_app.find_one({"token_app": token_app})['name_app'])
        except:
            return None

    def log_error(self, error):
        self.__handle.ses_error_log.insert({"error": error, "datetime": datetime.datetime.now()})