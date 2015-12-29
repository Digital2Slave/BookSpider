#-*- encoding:utf-8 -*-
"""
Name    : amazon spider
Author  : JohnTian
Date    : 12/18/2015
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
    #!< 书名
    name = ''
    bookname = sel.xpath('//span[@id="productTitle"]/text()').extract()
    kindlename = sel.xpath('//h1[@class="parseasinTitle"]/span/span/text()').extract()
    if (bookname != None) and (bookname != []):
        name = bookname[0]
    elif (kindlename != None and (kindlename != [])):
        name = kindlename[0]
    orderdict[u'书名'] = name.strip()

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
        orderdict[u'书籍封面'] = imgurl
    else:
        orderdict[u'书籍封面'] = ''

    #!< 用户评分
    score = ''
    try:
        #score = sel.xpath('//span[@id="acrPopover"]/@title').extract()
        score = sel.xpath('//div[@id="avgRating"]/span/text()').extract()
        if (score != []):
            score = score[0].strip()
        else: # kindle
            score = sel.xpath('//div[@class="gry txtnormal acrRating"]/text()').extract()
            if (score != []):
                score = score[0].strip()
    except:
        score = ''
    orderdict[u'用户评分'] = score

    #!< 亚马逊热销商品排名
    rank =''
    try: # book and kindle
        ranks = sel.xpath('//li[@id="SalesRank"]/text()').extract()
        if (ranks != []) and (len(ranks)>=2):
            for i in ranks[1]:
                if (' ' not in i) and ('\n' not in i) and ('(' not in i):
                    rank += i
    except:
        rank = ''
    orderdict[u'亚马逊热销商品排名'] = rank

    #!< 作者，出版社，原书名，译者，出版年，页数，定价，装帧，丛书，ISBN
    #!< 作者
    author = sel.xpath('//span[@class="author notFaded"]/a[@class="a-link-normal"]/text()').extract()
    authorlocation = sel.xpath('//span[@class="author notFaded"]/span/span[@class="a-color-secondary"]/text()').extract()
    authors = ''
    for i in range(len(author)):
        name0 = author[i]+authorlocation[i]
        authors += name0
    if (authors == ''):
        kindleauthor         = sel.xpath('//div[@class="buying"]/span/a/text()').extract()
        kindlelocationauthor = sel.xpath('//div[@class="buying"]/span/text()').extract()
        kindlelocation = ''
        if (kindlelocationauthor != None) and (kindlelocationauthor != []):
            kindlelocation = kindlelocationauthor[1].strip()
        for i in range(len(kindleauthor)):
            name1 = kindleauthor[i] + kindlelocation[i]
            authors += name1
    orderdict[u'作者'] = authors

    #!< 书籍其它信息
    detailNameTmp = sel.xpath('//div[@class="content"]/ul/li/b/text()').extract()
    detailName = [i.strip('\n :') for i in detailNameTmp]
    Name = detailName[:-2]

    detailValueTmp = sel.xpath('//div[@class="content"]/ul/li/text() | //div[@class="content"]/ul/li/a/text()').extract()
    detailValue = []
    for vt in detailValueTmp:
        vt = vt.strip('\n >')
        #if (vt != '') and (vt != u'\xa0'):
        detailValue.append(vt)
    Value = detailValue[:len(Name)]

    Num = len(Name)
    for i in xrange(Num):
        key = Name[i]
        val = Value[i]
        if (':' in key):
            key = key.strip(':')
        if (':' in val):
            val = val.strip(':')
        val = val.strip(' ')
        orderdict[key] = val
    #!< kindle
    try:
        xray = sel.xpath('//a[@id="xrayPop"]/span/text()').extract()
        orderdict['xRay'] = xray[0]
    except:
        orderdict['xRay'] = ''

    #!< 书籍价格
    PZprice = sel.xpath('//span[@class="a-button-inner"]/a/span/span/text()').extract()
    if (PZprice != []): # book
        if(len(PZprice)==1):
            price = PZprice[0].strip()
            orderdict[u'平装'] = price            #u'平装'
        else:
            price = [s.strip() for s in PZprice]
            orderdict[u'精装'] = price[0]          # u'精装'
            orderdict[u'平装'] = price[1]
    else:
        PZprice = sel.xpath('//b[@class="priceLarge"]/text()').extract()
        if (PZprice != []):
            price = PZprice[0].strip()
            orderdict[u'电子书价格'] = price

    #!< 内容简介 & 作者简介
    trees = sel.xpath('//div[@id="s_contents"]/div')
    infotitlelist = []
    infotitlevaluelist = []
    for tree in trees:
        #infotitle
        infotitle = checkXpathResult(tree.xpath('h3/text()').extract())
        infotitlelist.append(infotitle)

        #infotitlevalue
        # !< one
        tmpinfov = checkXpathResult(tree.xpath('div').extract())
        tmpinfovres = str()
        for v in tmpinfov:
            v = v.strip().encode('utf-8')
            tmpinfovres += v
        if ('<divclass="bbeditor">' in tmpinfovres):
            tmpinfovres = tmpinfovres.replace('<divclass="bbeditor">', '')
        if ('<br>' in tmpinfovres):
            tmpinfovres = tmpinfovres.replace('<br>', '')
        if ('<div>' in tmpinfovres):
            tmpinfovres = tmpinfovres.replace('<div>', '')
        if ('</div>' in tmpinfovres):
            tmpinfovres = tmpinfovres.replace('</div>', '')

        # !< two
        infotitlevalue = checkXpathResult(tree.xpath('p').extract())
        infotitlevalue = infotitlevalue.strip().encode('utf-8')
        if ('<p>' in infotitlevalue) or ('</p>' in infotitlevalue):
            infotitlevalue = infotitlevalue.replace('<p>','')
            infotitlevalue = infotitlevalue.replace('</p>','')
        if ('<br>' in infotitlevalue):
            infotitlevalue = infotitlevalue.replace('<br>','')

        # !< three
        res = infotitlevalue + ' ' + tmpinfovres
        infotitlevaluelist.append(res)

    #(k,v)
    if (infotitlelist != []) and (infotitlevaluelist != []):
        lenth = len(infotitlelist)
        for i in xrange(lenth-1):
            k, v = infotitlelist[i], infotitlevaluelist[i]
            orderdict[k] = v.strip()

    #!< 相关推荐书目
    simsbook = sel.xpath('//div[@id="purchase-sims-feature"]/div/@data-a-carousel-options').extract()
    bookasins = ''
    if (simsbook != []):
        data = simsbook[0]
        dataencode = data.encode('utf-8')
        r = re.compile('B\w{9,9}')
        bookasins = re.findall(r, dataencode)
    orderdict[u'相关推荐书目'] = bookasins          #u'相关推荐书目'

    #!< 书籍链接
    orderdict[u'书籍链接'] = bookurl

    return orderdict
