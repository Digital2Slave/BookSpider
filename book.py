"""
Name    : Book class
Author  : JohnTian
Date    : 12/18/2015
Version : 0.01
CopyLeft: OpenSource
"""
from config import *
from bookhelper import BookHelper
from spider import amazon, douban, GetAmazonBookCover


"""
    Book class for search book information from amazon or douban by one of \
    [isbn, asin, subjectid].
    Also, it gain book information by book title and author.
"""
class Book(BookHelper):

    def __init__(self, title=None, author=None, isbn=None, asin=None, subjectid=None):
        self.title      = title
        self.author     = author
        self.isbn       = isbn
        self.asin       = asin
        self.subjectid  = subjectid


    def getBookSubjectid(self):
        return self.subjectid

    def getAmazonBookInforByIsbn(self):
        isbn = self.isbn
        if (type(isbn) == str) and (isbn != ''):
            asin       = BookHelper(isbn=isbn).getAmazonAsinByIsbn()
            return amazon.parse(isbn, asin)
        else:
            return ''

    def getAmazonBookCoverByIsbn(self):
        isbn = self.isbn
        if (type(isbn) == str) and (isbn != ''):
            asin       = BookHelper(isbn=isbn).getAmazonAsinByIsbn()
            return GetAmazonBookCover.parse(isbn, asin)
        else:
            return ''

    def getAmazonBookInforByAsin(self):
        asin = self.asin
        if (type(asin)==str) and (asin != ''):
            isbn      = BookHelper(asin=asin).getAmazonIsbnByAsin()
            return amazon.parse(isbn, asin)
        else:
            return ''


    def getAmazonBookInforByTitleAndAuthor(self):
        title, author = self.title, self.author
        if (type(title)==str) and (type(author)==str) \
            and (title != '') and (author != ''):
            asin = BookHelper(title=title, author=author).getAmazonAsinByTitleAndAuthor()
            isbn = BookHelper(asin=asin).getAmazonIsbnByAsin()
            return amazon.parse(isbn, asin)
        else:
            return ''


    def getDoubanBookInforByIsbnOrSubjectId(self):
        isbn, subjectid = self.isbn, self.subjectid
        if (type(isbn) == str) and (isbn != ''):
            if (type(subjectid) == str) and (subjectid != ''):
                return douban.parse(isbn, subjectid)
            else:
                return douban.parse(isbn)
        elif (type(subjectid)==str) and (subjectid != ''):
            return douban.parse('', subjectid)
        else:
            return ''
