pymm
====

Python MassMailer is a simple tool helping to deliver a large number of
similar emails written in python3. Email message texts and attachments
can be costumized per recipient in an automatically generated
configuration file.

Usage
-----
    $ ./pymm.py -h
    Usage: pymm.py [options] cfgfile
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -i, --initialize      initialize an empty cfgfile and quit
      --initialize-with-github-note
                            initialize an empty cfgfile, add default git note and
                            quit
      -v                    show status messages (default)
      -q                    don't show status messages
      -V                    show debug messages
      
Workflow
--------
- Create *configfile* by
                    
          $ ./pymm.py -i configfile
    
- Edit *configfile*

- Execute *configfile* by
                     
        $ ./pymm.py configfile
