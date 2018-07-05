#!/usr/bin/env python

from atexit import register
from random import randrange
from threading import BoundedSemaphore,Lock,Thread
from time import sleep,ctime

lock = Lock()
MAX = 5
candytray = BoundedSemaphore(MAX)

def refill():
	lock.acquire() 
	print('Refilling candy...')
	try:
		candytray.release() #信号，压入资源

		print('OK')
	except ValueError:
		print('full,skiping')
	lock.release() 


def buy():
	lock.acquire()
	print('Buying candy...')
	if candytray.acquire(False):#信号，弹出资源
		print('Ok')
	else:
		print('empty,skiping')
	lock.release()

def produce(loops):
	for i in range(loops):
		refill()
		sleep(randrange(3))

def consumer(loops):
	for i in range(loops):
		buy()
		sleep(randrange(3))

def main():
	print('Starting at:',ctime())
	nloops = randrange(2,6)
	print('The candy machine (full with %d bars)!' % MAX)
	Thread(target = consumer,args=(randrange(nloops,nloops+MAX+2),)).start()
	Thread(target = produce,args = (nloops,)).start()

@register
def _atexit():
	print('all DONE at:',ctime())

if __name__ == '__main__':
	main()
