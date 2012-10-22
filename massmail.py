## 
##  massmail.py
## 
##   Created on: Oct 21, 2012
##       Author: martinez
##

import configparser
import re

from sendmail import send_mail

import logging
logger = logging.getLogger('pymm')

class MassMail:
  """MassMail"""

  @staticmethod
  def init_cfg_file(cfgfile, note=''):
    """Initialize a new config file with default values"""
    config = configparser.ConfigParser()
    config['DEFAULT'] = { 'username'     : 'user',
                          'senderadress' : 'me@you.com',
                          'mailhost'     : 'host.url.com',
                          'port'         : 25,
                          'subject'      : 'mail subject',
                          'message'      : 'message text {} {}',
                          'note'         : note }

    config['RECIPIENTS'] = { 'recipients': ['receiver1@url.com fmtstr1 fmtstr2 fileattachment1 fileattachment1',
                                            'receiver2@url.com fmtstr1 fmtstr2 fileattachment1',
                                            '...'] }
    
    with open(cfgfile, 'w') as configfile:
      config.write(configfile)
      logger.info('Initialized a plain new configuration %s.' % cfgfile)
      return

    logger.error('ERROR: Something went wrong writing plain new configuration %s.'
                 % cfgfile)
    sys.exit(1)

  def __init__(self, cfgfile):
    self.cfgfile = cfgfile

    config = configparser.ConfigParser()
    config.read(cfgfile)
    
    username     = config['DEFAULT']['username']
    senderadress = config['DEFAULT']['senderadress']
    mailhost     = config['DEFAULT']['mailhost']
    port         = config['DEFAULT']['port']
    subject      = config['DEFAULT']['subject']
    note         = config['DEFAULT']['note']

    # determine number of required fmtstr's in message
    message    = config['DEFAULT']['message']
    numfmtstrs = len(re.findall('{}',message))

    recipients = eval(config['RECIPIENTS']['recipients'])

    logger.debug('username: {}\n'
                 'senderadress: {}\n'
                 'mailhost: {}\n'
                 'port: {}\n'
                 'subject: {}\n'
                 'note: {}\n'
                 'message: {}\n'
                 'numfmtstrs: {}\n'
                 'recipients: {}'.format(username,senderadress,mailhost,port,
                                           subject,note,message,numfmtstrs,
                                           recipients))

    for recipient in recipients:
      data = recipient.strip().split()

      try:
        mail_dest   = data[0]
        fmtstrs     = data[1:numfmtstrs+1]
        attachments = data[numfmtstrs+1:]

        logger.debug('mail_dest: {}\n'
                     'fmtstrs: {}\n'
                     'attachments: {}'.format(mail_dest,fmtstrs,attachments))

        if(len(fmtstrs) != numfmtstrs):
          raise IndexError

        fmtmessage = message.format(*fmtstrs)
        logger.debug('fmtmessage: {}'.format(fmtmessage))

        send_mail(senderadress, mail_dest, subject, fmtmessage,
                  files=attachments, server=mailhost, user=username,
                  password=None, port=port, note=note)

      except IndexError as e:
        logger.warning('Skipping wrongly formated data {}: {}\n{}'.format(data,fmtstrs,e))
        continue
      except Exception as e:
        logger.warning('Error sending {}: {}'.format(data,e))
        continue

      logger.info('Mail to {} successfully send.'.format(mail_dest))