#!/usr/bin/env python3
#-*- coding: utf-8 -*-

text = ['hej','mu','fui','feng']

' '.join(text)

'-'.join(text)

print(a + ':' + b + ':' + c) # Ugly
print(':'.join([a, b, c])) # Still ugly
print(a, b, c, sep=':') # Better

def sample():
  yield 'Is'
  yield 'You'
  yield 'Beautiful'
  
def compute(source,maxsize):
  parts=[]
  size=0
  for part in source:
    parts.append(part)
    size+=len(part)
    if size >= maxsize:
      yield ' '.join(parts)
      parts = []
      size=0
    yield ' '.join(parts)
    
  with open(filename) as f:
    for part in compute(sample,32264):
      f.write(part)
      
