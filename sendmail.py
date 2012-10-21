## 
##  sendmail.py
## 
##   Created on: Oct 21, 2012
##       Author: martinez
##

import smtplib
import os
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

import logging
logger = logging.getLogger('pymm')

g_pw   = None
g_user = None

def send_mail(send_from, send_to, subject, text, files=[], server='localhost',
              user=None, password=None, port=25, note=''):
  assert type(files) == list

  logger.debug('sending to {}'.format(send_to))

  msg            = MIMEMultipart()
  msg['From']    = send_from
  msg['To']      = send_to
  msg['Date']    = formatdate(localtime=True)
  msg['Subject'] = subject

  if(note):
    msg.attach( MIMEText(text + '\n\n' + note) )
  else:
    msg.attach( MIMEText(text) )  
  
  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' %
                     os.path.basename(f))
    msg.attach(part)

  global g_pw, g_user

  if g_user == None:
    g_user = user

  if g_user == None:
    g_user = getpass.getuser('SMTP username for {}:'.format(server))

  if g_pw == None:
    g_pw = password

  if g_pw == None:
    g_pw = getpass.getpass('SMTP password for {}@{}:'.format(g_user,server))
      
  smtp = smtplib.SMTP(server, port)
  smtp.starttls()
  smtp.login(g_user, g_pw)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()