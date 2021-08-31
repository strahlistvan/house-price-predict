# -*- coding: utf-8 -*-
"""
Created on Sun NOV 27 16:27:14 2020

@author: strahl
"""

from datetime import datetime
from pymongo import MongoClient

class MongoDAO:

    fetchdate = datetime.now()
    collname = 'fetch-'+str(fetchdate)

    def __init__(self, conn_url='mongodb://localhost:27017', dbname='house_price_predict', fetchdate = datetime.now(), collname=None):
        self.fetchdate = fetchdate
        self.client = MongoClient(conn_url)
        self.db = self.client[dbname]
        if collname == None:
            self.collname = 'fetch-'+str(self.fetchdate)
        else:
            self.collname = collname
        self.collection = self.db[self.collname]

    def insert_documents(self, document_list):
        new_result = self.collection.insert_many(document_list, ordered=False)
        #print('Multiple posts: {0}'.format(new_result.inserted_ids))

    def get_all_documents(self, collection_name):
        return list(self.db[collection_name].find({}))

    def get_all_collection_names(self):
        return self.db.list_collection_names()
