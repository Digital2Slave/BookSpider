#-*- coding:utf-8 -*-
"""
Name    : douban spider
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

#!< 单独处理每一本书籍信息
def parse(isbn, subjectid=None):
    url = ''
    if (type(isbn)==str) and (isbn!=''):
        url = "http://book.douban.com/isbn/" + isbn
    elif(type(subjectid)==str) and (subjectid!=''):
        url = "http://book.douban.com/subject/" + subjectid
    else:
        raise "Check the input isbn or douban subjectid str value!"
        return None

    sel, page, bookurl, urlstate = getSelPagebyUrl(url)

    # OrderedDict的Key会按照插入的顺序排列
    orderdict = OrderedDict()

    #!< 书名，书籍封面URL，评分
    title  = sel.xpath('//div[@id="wrapper"]/h1/span/text()').extract()
    if (title !=[]):
        orderdict[u'书名'] = title[0]
    else:
        orderdict[u'书名'] = ''

    coverurlTmp = sel.xpath('//div[@id="mainpic"]/a/img/@src').extract()
    coverurl = str()
    if (coverurlTmp != []):
        coverurlv = coverurlTmp[0]
        if ('mpic' in coverurlv):
            coverurl = coverurlv.replace('mpic','lpic')
    orderdict[u'书籍封面'] = coverurl

    rateTmp1 = sel.xpath('//div[@class="rating_wrap"]/p/strong/text()').extract()
    rateTmp2 = sel.xpath('//strong[@class="ll rating_num "]/text()').extract()
    rate = str()
    if (rateTmp1 != []):
        rate = rateTmp1[0].strip()
    elif(rateTmp2 != []):
        rate = rateTmp2[0].strip()
    else:
        pass

    orderdict[u'评分'] = rate

    #!< 作者，出版社，原书名，译者，出版年，页数，定价，装帧，丛书，ISBN
    sels = sel.xpath('//div[@id="info"]/span')

    for tree in sels:

        tv = tree.xpath('text()').extract()
        tv = tv[0].strip(':') if (tv!=[]) else ('') # title value

        # 作者，译者
        tvs = tree.xpath('span/text()').extract()
        tvs = tvs[0].strip() if (tvs!=[]) else ('')
        if (tvs != ''):
            tv = tvs

        # 其他
        afind = str()
        afind = tree.xpath('following-sibling::text()').extract_first().strip()

        if (afind == ''):
            # 作者，译者
            av = tree.xpath('a/text()').extract()
            av = av[0].strip() if (av!=[]) else ('') # <a> text </a>
            if (av == ''):
                # 丛书
                avs = sel.xpath('//div[@id="info"]/a/text()').extract()
                avs = avs[0].strip() if (avs!=[]) else ('')
                afind = avs
            else:
                afind = av
        orderdict[tv] = afind


    #!< 内容简介 & 作者简介
    titles = sel.xpath('//div[@class="related_info"]/h2')
    values = sel.xpath('//div[@class="related_info"]/div')

    if (values != []):

        lenth = len(titles) if (len(titles)<=len(values)) else len(values)
        flag = True if (values[0].xpath('div[@class="ebook-promotion"]')) else False

        if flag:
            for i in xrange(lenth):

                title = titles[i]
                t = title.xpath('span/text()').extract()
                t = t[0] if (t!=[]) else ('')

                content = list()
                if (values[i].xpath('div[@class="ebook-promotion"]')):

                    contenttmp = values[i+1].xpath('span[@class="all hidden"]/div/div[@class="intro"]/p/text()').extract()
                    if contenttmp:
                        content = contenttmp
                    else:
                        content = values[i+1].xpath('div/div[@class="intro"]/p/text()').extract()

                else:

                    contenttmp = values[i+1].xpath('span[@class="all hidden"]/div/div[@class="intro"]/p/text()').extract()
                    if contenttmp:
                        content = contenttmp
                    else:
                        content = values[i+1].xpath('div/div[@class="intro"]/p/text()').extract()

                if (i<2):
                    orderdict[t] = content
        else:
            for i in xrange(lenth):
                title = titles[i]
                t = title.xpath('span/text()').extract()
                t = t[0] if (t!=[]) else ('')

                content = list()
                contenttmp = values[i].xpath('span[@class="all hidden"]/div/div[@class="intro"]/p/text()').extract()
                if contenttmp:
                    content = contenttmp
                else:
                    content = values[i].xpath('div/div[@class="intro"]/p/text()').extract()
                orderdict[t] = content

    #!< 标签
    tags = sel.xpath('//div[@class="indent"]/span/a/text()').extract()
    tags = tags if (tags != []) else ('')
    orderdict[u'标签'] = tags

    #!< 相关推荐书目
    recom = sel.xpath('//div[@class="content clearfix"]/dl/dt/a/@href').extract()
    if (recom != []):
        subjectid = [ s[-9:-1] for s in recom]
        orderdict[u'相关推荐书目'] = subjectid
    else:
        orderdict[u'相关推荐书目'] = ''

    #!< 书籍购买来源
    buybook = sel.xpath('//ul[@class="bs noline more-after "]/li/a/@href').extract()
    buybook = buybook if (buybook != []) else ('')
    orderdict[u'书籍购买来源'] = buybook

    #!< 书籍链接
    bookurl  = bookurl
    urlstate = urlstate

    orderdict[u'书籍链接'] = bookurl

    return orderdict
