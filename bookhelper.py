#-*- coding:utf-8 -*-
"""
Name    : BookHelper class
Author  : JohnTian
Date    : 12/18/2015
Version : 0.01
CopyLeft: OpenSource
"""
from config import *
import random, requests, re
from scrapy import Selector
from urllib2 import urlopen,Request
from requests.auth import HTTPProxyAuth

import sys, time, json
sys.setrecursionlimit(250)

"""
    Get useragentstring for urllib2.Request.
"""
def getUserAgentString(useragent=USER_AGENT):
    user_agent_list = ''
    if (type(useragent)==str) and (useragent.endswith('.json')):
        #http://www.useragentstring.com/pages/useragentstring.php
        browerfile = file(useragent, 'rb')
        browerdata = json.load(browerfile)
        browerfile.close()

        PCbrower        = browerdata['brower']      #9502
        MBbrower        = browerdata['mobilebrower']#512
        user_agent_list = PCbrower+MBbrower
    elif (type(useragent)==list):
        user_agent_list = useragent
    else:
        raise "useragent must be json file or list of useragentstring!"
        return ''
    return random.choice(user_agent_list)


"""
    Get url's sel, page, url, request status by proxy.
"""
def getSelPagebyUrlProxy(url):
    headers    = {}
    proxy_auth = HTTPProxyAuth(USER_KEY, "")
    proxies    = {"http": "http://{}:8010/".format(PROXY_HOST)}

    if url.startswith("https:"):
        url = "http://" + url[8:]
        headers["X-Crawlera-Use-HTTPS"] = "1"

    req    = requests.get(url, headers=headers, proxies=proxies, auth=proxy_auth)
    page   = req.text
    status = req.status_code
    sel    = Selector(text=page)

    return sel, page, url, status


"""
    Get url's sel, page, url, request status by useragent.
"""
def getSelPagebyUrl(url):
    useragentstring = getUserAgentString(useragent=USER_AGENT)
    request_headers = { 'User-Agent': useragentstring }
    request         = Request(url, None, request_headers)
    if (request!=None):
        req     = urlopen(request, timeout=60)
        page    = req.read()
        status  = req.getcode()
        sel     = Selector(text=page)
        return sel, page, url, status
    else:
        time.sleep(1)
        return getSelPagebyUrl(url)


"""
    Get amazon book's asin by isbn.
"""
def AmazonIsbn2Asin(isbn):
    url = 'http://www.amazon.cn/s/ref=nb_sb_noss?field-keywords=' + isbn
    sel, page, url, status = getSelPagebyUrl(url)

    nores = sel.xpath('//h1[@id="noResultsTitle"]/text()').extract()
    if nores:
        return '' #not found!
    else:
        res = sel.xpath('//li[@id="result_0"]/@data-asin').extract()
        if res:
            return res[0]
        else:
            time.sleep(1)
            return AmazonIsbn2Asin(isbn)


"""
    Get amzon book's asin by title and author.
"""
def AmazonTitleAndAuthor2Asin(title, author):
    index = title + ' ' + author
    url = 'http://www.amazon.cn/s/ref=nb_sb_noss?field-keywords=' + index
    sel, page, url, status = getSelPagebyUrl(url)

    nores = sel.xpath('//h1[@id="noResultsTitle"]/text()').extract()
    if nores:
        return '' #not found!
    else:
        res = sel.xpath('//li[@id="result_0"]/@data-asin').extract()
        if res:
            return res[0]
        else:
            time.sleep(1)
            return AmazonTitleAndAuthor2Asin(title, author)


"""
    Get amazon book's isbn by asin.
"""
def AmazonAsin2Isbn(asin):
    url  = 'http://www.amazon.cn/dp/' + asin

    sel, page, url, status = getSelPagebyUrl(url)

    risbn    = re.compile(r'<b>ISBN:</b>[\d, ]*</li>')
    rbarcode = re.compile(r'<b>条形码:</b>[\d ]*</li>')
    barcode  = re.findall(rbarcode, page)
    isbnval  = re.findall(risbn, page)

    isbn = ''
    if (barcode != []):
        length = len('<b>\xe6\x9d\xa1\xe5\xbd\xa2\xe7\xa0\x81:</b>')
        isbn = barcode[0][length:-5].strip()
    elif (isbnval != []):
        isbn = isbnval[0][13:-5].strip()
    else:
        isbn = ''
    return isbn


"""
    BookHelper class for search amzon book's isbn or asin!
"""
class BookHelper:

    def __init__(self, title=None, author=None, isbn=None, asin=None):
        self.title   = title
        self.author  = author
        self.isbn    = isbn
        self.asin    = asin

    def getBookTitle(self):
        return self.title

    def getBookAuthor(self):
        return self.author

    def getBookIsbn(self):
        return self.isbn

    def getBookAsin(self):
        return self.asin

    def getAmazonAsinByIsbn(self):
        isbn = self.isbn
        if (type(isbn) == str) and (isbn != ''):
            asin      = AmazonIsbn2Asin(isbn)
            return asin
        else:
            return ''

    def getAmazonIsbnByAsin(self):
        asin = self.asin
        if (type(asin) == str) and (asin != ''):
            isbn      = AmazonAsin2Isbn(asin)
            return isbn
        else:
            return ''

    def getAmazonAsinByTitleAndAuthor(self):
        title, author = self.title, self.author
        if (type(title)==str) and (type(author)==str) and (title != '') and (author != ''):
            asin = AmazonTitleAndAuthor2Asin(title, author)
            return asin
        else:
            return ''
