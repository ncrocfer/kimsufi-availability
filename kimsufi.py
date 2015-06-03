#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find the Kimsufi servers availability.

Usage:
  kimsufi.py [options]
  kimsufi.py <model>... [options]

Options:
  -h, --help     Show this help.
  -v, --version  Show version.
  -m, --mail     Sends a mail when a server is available.

Examples:
  kimsufi.py
  kimsufi.py KS-1 KS-3
  kimsufi.py KS-1 --mail
"""

import sys
import smtplib

import requests
import json
import os

from docopt import docopt

VERSION = "1.0"

API_URL = "https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2"
REFERENCES = REFERENCES = {
  "150sk10": "KS-1",
  "150sk20": "KS-2",
  "150sk21": "KS-2",
  "150sk22": "KS-2 SSD",
  "150sk30": "KS-3",
  "150sk31": "KS-3",
  "150sk40": "KS-4",
  "150sk41": "KS-4",
  "150sk42": "KS-4",
  "150sk50": "KS-5",
  "150sk60": "KS-6",

  "141game1": "GAME-1",
  "141game2": "GAME-2",
  "141game3": "GAME-3",

  "142sys4":  "SYS-IP-1",
  "142sys5":  "SYS-IP-2",
  "142sys8":  "SYS-IP-4",
  "142sys6":  "SYS-IP-5",
  "142sys10": "SYS-IP-5S",
  "142sys7":  "SYS-IP-6",
  "142sys9":  "SYS-IP-6S",

  "143sys13": "E3-SSD-1",
  "143sys10": "E3-SSD-2",
  "143sys11": "E3-SSD-3",
  "143sys12": "E3-SSD-4",
  
  "143sys4":  "E3-SAT-1",
  "143sys1":  "E3-SAT-2",
  "143sys2":  "E3-SAT-3",
  "143sys3":  "E3-SAT-4",
  
  "141bk1":   "BK-8T",
  "141bk2":   "BK-24T"
}

ZONES = {'gra': 'Gravelines',
         'sbg': 'Strasbourg',
         'rbx': 'Roubaix',
         'bhs': 'Beauharnois'}

CURRENT_PATH = os.path.dirname(__file__)

def get_city_name(zone):
	# rbx-hz to rbx
	zone = zone.split('-')[0]
	if zone in ZONES:
		return ZONES[zone]
	else:
		return zone

def get_servers(models):
	"""Get the servers from the OVH API."""
	
	r = requests.get(API_URL)
	response = r.json()['answer']['availability']
	
	search = REFERENCES
	if models:
		search = {k: v for k, v in REFERENCES.items() if v in models}
		
	return [k for k in response if any(r == k['reference'] for r in search)]


def get_ref(name):
	"""Return the reference based on the server model."""
	
	return list(REFERENCES.keys())[list(REFERENCES.values()).index(name)]


def send_mail(output, total):

	try:
		with open(os.path.join(CURRENT_PATH,'config.json')) as data:
			config = json.load(data)
			mail_host = config['email']['host']
			mail_port = config['email']['port']
			mail_username = config['email']['username']
			mail_password = config['email']['password']
			mail_from = config['email']['mail']
			mail_to = config['email']['mail']

	except IOError:
		print('Rename config.json.sample to config.json and edit it')
		return False

	"""Send a mail to <mail_to>."""
	
	subject = "{0} server{1} {2} available on Kimsufi".format(
		total,
		"s"[total<=1:],
		["is", "are"][total>1]
	)
	headers = "From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n".format(
		mail_from,
		mail_to,
		subject
	)
	
	try:
		server = smtplib.SMTP(mail_host, mail_port)
	except smtplib.socket.gaierror:
		return False
	
	server.ehlo()
	server.starttls()
	server.ehlo()
	
	try:
		server.login(mail_username, mail_password)
	except smtplib.SMTPAuthenticationError:
		print('SMPT Auth Error!')
		return False
	
	try:
		server.sendmail(mail_from, mail_to, headers + output)
		return True
	except Exception:
		print('Error sending email!')
		return False
	finally:
		server.close()


if __name__ == '__main__':
	arguments = docopt(__doc__, version=VERSION)
	kim = get_servers(arguments['<model>'])

	total = 0
	output = ""
	
	for k in kim:
		output += "\n{}\n".format(REFERENCES[k['reference']])
		output += "{}\n".format("="*len(REFERENCES[k['reference']]))
		
		for z in k['zones']:
			invalids = ['unavailable', 'unknown']
			availability = z['availability']
			if not availability in invalids:
				total += 1
			output += '{} : {}\n'.format(get_city_name(z['zone']), availability)
	
	output += "\n=======\nRESULT : {0} server{1} {2} available on Kimsufi\n=======\n".format(
		total,
		"s"[total<=1:],
		["is", "are"][total>1]
	)
	
	if total != 0 :
		if arguments['--mail']:
			print(output)
			send_mail(output, total)
		else:
			print(output)
