#!/usr/bin/env pyhton
from atexit import register
from re import compile
from threading import Thread
from time import ctime
from urllib.request import urlopen as uopen


REGEX = compile(r'#([\d,]+) in Books')
AMZN = 'http://www.amazon.com/'
ISBNs = {
	's?field-keywords=0132269937':'Core Python Programming',
#	's?field-keywords=0132269937',
#       's?field-keywords=0132356139'
	's?field-keywords=0132356139':'Python Web Development with Django',
	's?field-keywords=0137143419':'Python Fundamentals',
}


def getRanking(isbn):
	page = uopen('%s%s' % (AMZN,isbn))
	data = page.read().decode('utf-8')
	page.close()
	return REGEX.findall(data)[0]

def _showRanking(isbn):
	print('-%s ranked %s ' % (ISBNs[isbn],getRanking(isbn)))

def _main():
	print('At' ,ctime(),'on amazon...')
	for isbn in ISBNs:
		_showRanking(isbn)

#@register
def _atexit():
	print('all Done at:',ctime())

if __name__ =='__main__':
       	_main()
