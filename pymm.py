#!/usr/bin/python3

## 
##  pymm.py
## 
##   Created on: Oct 21, 2012
##       Author: martinez
##

import sys
import codecs

import logging
from coloredformatter import ColoredFormatter

import optparse
import configparser

# (colored) logging
logger = logging.getLogger(sys.argv[0])

# mailing
class MassMail:
  """MassMail"""

  @staticmethod
  def init_cfg_file(cfgfile):
    """Initialize a new config file with default values"""
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Username': 'user',
                         'Mailhost': 'host.url.com',
                         'Subject':  'mail subject',
                         'Message':  'message text {} {}'}

    config['RECIPENTS'] = {'Recipents': ['receiver1@url.com fmtstr1 fmtstr2 attachment1 attachment1',
                                         'receiver2@url.com fmtstr1 fmtstr2 attachment1 attachment2',
                                         '...']}
    
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
    
    logger.debug('recipents: {}'.format(config['RECIPENTS']['recipents']))
    
    recipents = config['RECIPENTS']['recipents']



    for recipent in recipents:
      print(recipent)
      # line = recipent.strip().split()
      # logger.debug("%s"%recipent)
      # mail_dest = line[0]
      # attachments = line[1:]
            
    #         print(line)
            
    #         try:
    #             send_mail(SENDER, mail_dest, SUBJECT, MESSAGE,
    #                       attachments, server=MAILHOST, user=USER, note=NOTE)
    #         except Exception as e:
    #             print(e)
    #             print('Warning: Could not send email to', mail_dest)
                
    #         print('Mail to', mail_dest, 'successfully send with attachments', str(attachments))    

if __name__ == "__main__":
  logger.setLevel(logging.WARNING)
  console = logging.StreamHandler()
  console.setFormatter(
    ColoredFormatter('%(name)s: %(message)s (%(filename)s:%(lineno)d)'))
  logger.addHandler(console)

  parser = optparse.OptionParser(usage="usage: %prog [options] cfgfile")
  parser.add_option("-i", "--initialize",
                    action="store_true", dest="initialize",
                    help="initialize an empty cfgfile and quit")
  parser.add_option("-v", action="store_true",  dest="verbose",
                    help="show status messages (default)")
  parser.add_option("-q", action="store_false", dest="verbose",
                    help="don't show status messages")
  parser.add_option("-V", action="store_true",  dest="debug",
                    help="print debug messages")

  parser.set_defaults(initialize=False,
                      verbose=True, debug=False)

  (options, args) = parser.parse_args()

  if(options.verbose):
    logger.setLevel(logging.INFO)
  if(options.debug):
    logger.setLevel(logging.DEBUG)

  # logger.debug('debug')
  # logger.info('info')
  # logger.warning('Warning')
  # logger.error('ERROR')
  # logger.critical('CRITICAL!!!')

  if(len(args) != 1):
    logger.error('ERROR: Require config file.')
    sys.exit(1)

  cfgfile = args[0]

  logger.debug(str(args))
  logger.debug(str(options))

  if(options.initialize):
    MassMail.init_cfg_file(cfgfile)
    sys.exit(0)

  mm = MassMail(cfgfile)
