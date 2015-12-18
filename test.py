#-*- coding:utf-8 -*-
"""
Name    : test
Author  : JohnTian
Date    : 12/18/2015
Version : 0.01
CopyLeft: OpenSource
"""
import os
from book import Book
from bookhelper import BookHelper

#!< BookHelper class.
"""
    BookHelper.getAmazonAsinByIsbn test.
"""
def test1(bookhelper, target):
    if (bookhelper.getAmazonAsinByIsbn()==target):
        print bookhelper.getBookIsbn()
        print 'test1 pass...'
    else:
        print 'BookHelper.getAmazonAsinByIsbn not pass!'


"""
    BookHelper.getAmazonIsbnByAsin test.
"""
def test2(bookhelper, target):
    if (bookhelper.getAmazonIsbnByAsin()==target):
        print bookhelper.getBookAsin()
        print 'test2 pass...'
    else:
        print 'BookHelper.getAmazonIsbnByAsin not pass!'


"""
    BookHelper.getAmazonAsinByTitleAndAuthor test.
"""
def test3(bookhelper, target):
    if (bookhelper.getAmazonAsinByTitleAndAuthor()==target):
        print bookhelper.getBookTitle()
        print bookhelper.getBookAuthor()
        print 'test3 pass...'
    else:
        print 'BookHelper.getAmazonAsinByTitleAndAuthor not pass!'


#!< Book class.
"""
    Book.getAmazonBookInforByIsbn test.
"""
def test4(book):
    bookdict = book.getAmazonBookInforByIsbn()
    if (bookdict != ''):
        # for (k,v) in bookdict.items():
        #     print k, v
        print book.getBookIsbn()
        print 'test4 pass...'
    else:
        print 'Book.getAmazonBookInforByIsbn not pass!'


"""
    Book.getAmazonBookInforByAsin test.
"""
def test5(book):
    bookdict = book.getAmazonBookInforByAsin()
    if (bookdict != ''):
        # for (k,v) in bookdict.items():
        #     print k, v
        print book.getBookAsin()
        print 'test5 pass...'
    else:
        print 'Book.getAmazonBookInforByAsin not pass!'


"""
    Book.getAmazonBookInforByTitleAndAuthor test.
"""
def test6(book):
    bookdict = book.getAmazonBookInforByTitleAndAuthor()
    if (bookdict != ''):
        # for (k,v) in bookdict.items():
        #     print k, v
        print book.getBookTitle()
        print book.getBookAuthor()
        print 'test6 pass...'
    else:
        print 'Book.getAmazonBookInforByTitleAndAuthor not pass!'


"""
    Book.getDoubanBookInforByIsbnOrSubjectId isbn test.
"""
def test7(book):
    bookdict = book.getDoubanBookInforByIsbnOrSubjectId()
    if (bookdict != ''):
        # for (k,v) in bookdict.items():
        #     print k, v
        print book.getBookIsbn()
        print 'test7 pass...'
    else:
        print 'Book.getDoubanBookInforByIsbnOrSubjectId isbn not pass!'


"""
    Book.getDoubanBookInforByIsbnOrSubjectId subjectid test.
"""
def test8(book):
    bookdict = book.getDoubanBookInforByIsbnOrSubjectId()
    if (bookdict != ''):
        # for (k,v) in bookdict.items():
        #     print k, v
        print book.getBookSubjectid()
        print 'test8 pass...'
    else:
        print 'Book.getDoubanBookInforByIsbnOrSubjectId subjectid not pass!'




if (__name__=='__main__'):

    print 'Test begin......'
    print '*'*179
    #BookHelper Amazon
    isbn1 = '9787111326533'
    asin1 = 'B004TUJ7A6'

    asin2 = 'B00WKR1OKG'
    isbn2 = '9787115379597'

    title  = '利用Python进行数据分析'
    author = '麦金尼 (Wes McKinney) (作者), 唐学韬 (译者), 等 (译者)'
    asin3  = 'B00GHGZLWS'

    bookhelper1 = BookHelper(isbn=isbn1)
    bookhelper2 = BookHelper(asin=asin2)
    bookhelper3 = BookHelper(title=title, author=author)
    test1(bookhelper1, asin1)
    test2(bookhelper2, isbn2)
    test3(bookhelper3, asin3)

    print 'BookHelper test work done!!!'
    print '*'*179

    #Book Amazon
    book1 = Book(title=None, author=None, isbn=isbn1, asin=None, subjectid=None)
    book2 = Book(title=None, author=None, isbn=None, asin=asin2, subjectid=None)
    book3 = Book(title=title, author=author, isbn=None, asin=None, subjectid=None)

    #Book Douban
    isbn4 = '9787549571413'
    subjectid = '26598484'
    book4 = Book(title=None, author=None, isbn=isbn4, asin=None, subjectid=None)
    book5 = Book(title=None, author=None, isbn=None, asin=None, subjectid=subjectid)

    test4(book1)
    test5(book2)
    test6(book3)
    test7(book4)
    test8(book5)

    print 'Book test work done!!!'
    print '*'*179

    print 'end......'
