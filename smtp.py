#!/usr/bin/env python
import asyncore
import email
from datetime import datetime
from smtpd import SMTPServer
from base64 import b64decode
from yaml import load

savemsg = True

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class XARFServer(SMTPServer):
	no = 0
	def process_message(self, peer, mailfrom, rcpttos, data):
		if savemsg:
			filename = 'savedmsg/%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'), self.no)
			f = open(filename, 'w')
			f.write(data)
			f.close

		if 'X-Arf: yes' in data:
			mail = email.message_from_string(data)

			for part in mail.walk():
				ctypes = part.get_params(None, 'Content-Type')
				if ctypes and len(ctypes) > 2:
					if ctypes[0] == ('text/plain', '') and ctypes[2] == ('name', 'report.txt'):
						payload = part.get_payload()
						xarf = load(payload, Loader=Loader)
						handle_xarf(xarf)

				dtypes = part.get_params(None, 'Content-Disposition')
				if dtypes and dtypes[1] == ('filename', 'report.txt'):
					payload = b64decode(part.get_payload())
					xarf = load(payload, Loader=Loader)
					handle_xarf(xarf)

		print 'Email received at %s' % datetime.now().strftime('%H:%M:%S')
		self.no += 1

def handle_xarf(xarf):
	### DO SOMETHING WITH THIS X-ARF ###
	print xarf

def run():
	print 'Python SMTP server'
	print 'Quit the server with CONTROL-C.'
	foo = XARFServer(('0.0.0.0', 25), None)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		pass


if __name__ == '__main__':
	run()
