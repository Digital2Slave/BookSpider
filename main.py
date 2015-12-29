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

import json, time
import pymongo
from pymongo import MongoClient
from optparse import OptionParser

from multiprocessing import Pool

def isbn2bookdata(isbn):
    # for isbn in data:
    asin  = AmazonIsbn2Asin(isbn)
    if (asin != ''):
        bookdict = GetAmazonBookCover.parse(isbn, asin)
        item     = {}
        item['bookinfo'] = bookdict
        return item

def bookdata2mongoData(item):
    if item != None:
        # !< connect mongodb
        client    = MongoClient(host=MONGODB_SERVER, port=MONGODB_PORT)
        db        = client[MONGODB_DB]
        bookcover = db[MONGODB_COLLECTION]
        bookcover.update({'bookinfo':item['bookinfo']}, item, upsert=True)

def run(data):
    pool = Pool(4)
    items = pool.map(isbn2bookdata, data)
    pool.close()
    pool.join()

    pool = Pool(4)
    pool.map(bookdata2mongoData, items)
    pool.close()
    pool.join()


def test(data):
    # spark given number of processes
    print 'start......'
    pool = Pool(4)
    t1 = time.time()
	# map to pool
    items = pool.map(isbn2bookdata, data)
    pool.close()
    pool.join()
    t2 = time.time()
    print t2-t1
    print 'bookdata done...'

    pool = Pool(4)
    pool.map(bookdata2mongoData, items)
    pool.close()
    pool.join()
    t3 = time.time()
    print t3-t2
    print 'mongodata done...'


if __name__=='__main__':
    '''
    Usage :
    $ python <name>.py --input=<isbnspath>
    eg:
    $ python main.py --input='./file/data/isbns_i.json'
    '''
    parser = OptionParser()
    parser.add_option("-i", "--input", action="store", dest="isbnData", help="Load isbn file.")
    (options,args) = parser.parse_args()
    filename       = options.isbnData

    # !< load data
    with open(filename, 'rb') as fi:
        data = json.load(fi)
    fi.close()

    step = 100
    splitdatas = [data[i:i+step] for i in xrange(0,len(data),step)]

    for d in splitdatas:
        run(d)
        time.sleep(3)
