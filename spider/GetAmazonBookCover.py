#-*- encoding:utf-8 -*-
"""
Name    : amazon spider
Author  : JohnTian
Date    : 12/27/2015
Version : 0.01
CopyLeft: OpenSource
"""
import sys
sys.path.append("..")

import re
from collections import OrderedDict
from bookhelper import getSelPagebyUrl, getSelPagebyUrlProxy

def checkXpathResult(rlist):
    if rlist != []:
        return rlist[0]
    else:
        return []

def parse(isbn, asin):
    #!!< bookurl !!!
    url = 'http://www.amazon.cn/dp/' + asin
    sel, page, bookurl, urlstate = getSelPagebyUrl(url)

    if (urlstate<200) or (urlstate>=400):
        return {'url':bookurl, 'isbn':isbn, 'asin':asin}

    #!!< 书籍信息字典 !!!
    orderdict = OrderedDict()
    orderdict['url'] = url
    orderdict['isbn'] = isbn
    orderdict['asin'] = asin

    #!< 书籍封面URL
    #1.books
    texturl = page
    #Re = r"http://ec4.images-amazon.com/images/I/[\w]+-?%?_?.?[\w]+.jpg"
    Re = r'''"mainUrl":"http://ec4.images-amazon.com/images/I/[\w]+.+[\w]+.jpg"'''
    imgurls = re.findall(Re, texturl)

    #2.kindle books
    kindleRe = r'''"large":"http://ec4.images-amazon.com/images/I/[\w]+.+[\w]+.jpg"'''
    kimgurls = re.findall(kindleRe, texturl)

    imgurl = str()
    if (imgurls != []):# be sure mainUrl in imgurls
        tmpimgurl = imgurls[0]
        stringval = '''","dimensions"'''
        if (stringval in tmpimgurl):
            endindex = tmpimgurl.find(stringval)
            imgurl = tmpimgurl[11:endindex]
        else:
            imgurl = tmpimgurl

    elif(kimgurls != []):# be sure large in imgurls
        tmpimgurl = kimgurls[0]
        stringval = '''","variant"'''
        if (stringval in tmpimgurl):
            endindex = tmpimgurl.find(stringval)
            imgurl = tmpimgurl[9:endindex]
        else:
            imgurl = tmpimgurl
    else:
        #raise ("Not cover!")
        imgurl = ''

    if (imgurl.startswith('http://ec4.images-amazon.com/images/I/')):
        #'http://ec8.images-amazon.com/images/I/91bpj-PbL1L.jpg'
        orderdict[u'image'] = imgurl
    else:
        orderdict[u'image'] = ''

    return orderdict
