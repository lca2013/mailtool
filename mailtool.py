#!/usr/bin/python

"""Send email blasts to lists of addresses

Sample use:
  ./mailtool.py --body=samplebody.txt --tolist=samplerecipients.txt \
  --subject="Testing 123"
"""

import datetime
import gflags
import smtplib
import sys


gflags.DEFINE_string('body', '', 'Body of email')
gflags.DEFINE_string('tolist', '',
                     'List of addresses to send to. One per line')
gflags.DEFINE_string('mailserver', 'localhost', 'Mail server to send to')
gflags.DEFINE_string('mailfrom', 'contact@lca2013.linux.org.au',
                     'Address to use as from address')
gflags.DEFINE_string('subject', '', 'Subject for the email')
FLAGS = gflags.FLAGS


def SendEmail(to, subject, body):
    s = smtplib.SMTP(FLAGS.mailserver)
    s.sendmail(FLAGS.mailfrom, [to],
             """From: %(from)s\r
To: %(to)s\r
Subject: %(subject)s\r
\r
%(body)s""" % {'from': FLAGS.mailfrom,
               'to': to,
               'subject': subject,
               'body': body})
    s.quit()


def main(argv):
    # Parse flags
    try:
        argv = FLAGS(argv)
        
    except gflags.FlagsError, e:
        print 'Flags error: %s' % e
        print
        print FLAGS

    if len(FLAGS.subject) == 0:
        print 'Set a subject!'
        sys.exit(1)
    if len(FLAGS.tolist) == 0:
        print 'Set a list of recipients!'
        sys.exit(1)
    if len(FLAGS.body) == 0:
        print 'Set an email body!'
        sys.exit(1)

    f = open(FLAGS.body, 'r')
    body = f.read()
    f.close()

    f = open(FLAGS.tolist, 'r')
    addresses = f.readlines()
    f.close()

    count = 0
    for address in addresses:
        address = address.rstrip()
        SendEmail(address, FLAGS.subject, body)
        count += 1
        print '%s: %d of %d sent' %(datetime.datetime.now(),
                                    count, len(addresses))
                                    

if __name__ == "__main__":
  main(sys.argv)
