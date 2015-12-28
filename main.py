#-*- coding:utf-8 -*-
"""
Name    : test
Author  : JohnTian
Date    : 12/18/2015
Version : 0.01
CopyLeft: OpenSource
"""
from config import *
from bookhelper import AmazonIsbn2Asin
from spider import GetAmazonBookCover
from collections import OrderedDict

import json
import pymongo
from pymongo import MongoClient
from optparse import OptionParser

if __name__=='__main__':
    '''
    Usage :
    $ python <name>.py --input=<isbnspath>
    eg:
    $ python main.py --input='./file/data/isbns_21.json'
    '''
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", dest="isbnData", help="Load isbn file.")
    (options,args) = parser.parse_args()
    filename       = options.isbnData

    # !< load data
    with open(filename, 'rb') as fi:
        data = json.load(fi)
    fi.close()

    # !< connect mongodb
    client    = MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
    db        = client[MONGODB_DB]
    bookcover = db[MONGODB_COLLECTION]

    # !< run
    cnt = 0
    for isbn in data:
        cnt += 1
        print cnt
        asin  = AmazonIsbn2Asin(isbn)
        if (asin != ''):
            bookdict = GetAmazonBookCover.parse(isbn, asin)
            item     = {}
            item['bookinfo'] = bookdict
            bookcover.update({'bookinfo':item['bookinfo']}, item, upsert=True)
