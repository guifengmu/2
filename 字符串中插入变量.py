#!/usr/bin/env python3
#-*— coding: utf-8 -*-

name = 'guifeng'
nu = '3'
s = '{name} has {nu} messages?'

s.fotmat_map(vars())
###vars()变量域
class Info:
  def __init__(self,name,nu):
    self.name=name
    self.nu=nu
    
a = Info('guifeng',3)
s.format_map(vars(a))
