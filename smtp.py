#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from smtplib import SMTP as smtp

from email import encoders
from email.utils import parseaddr,formataddr
from emil.mime.text import MIMEText
from email.header import Header

def _format_addr(s):
  name,addr = parseaddr(s)
  return formataddr(Header(name,'utf-8').encode(),addr)
  
from_addr= input('From:')
to_addr = input('To:')
smtp_server = input('smptserver:')
#password = input('Password:')

def main():
  ret = True
  try:
    msg = MIMEText('hello,this is text','plain','utf-8')
    msg['From'] = _format_addr('python爱好者<%s>' % from_addr)
    msg['To'] = _format_addr('管理员<%s>' % to_addr)
    msg['Subject'] = Header('这是测试邮件。。。','utf-8').encode()
    
    server = smtp(smtp_server)
    server.set_debuglevel(1)
    #server.login(from_addr,password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()
  except Exception:
    ret = False
  retrun ret
  
  
ret = main()

if ret:
  print('邮件发送成功')
else:
  print('邮件发送失败')
  
