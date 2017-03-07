#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ConfigParser

class User:
	
	username = ''
	accountID = ''
	password = ''

	twilioID = ''
	twilioToken = ''

	phNumber_from = ''
	phNumber_to = ''

	target_subject = ''

	def __init__(self):

		cp = ConfigParser.SafeConfigParser()
		cp.read('user.cfg')

		self.username = cp.get('user', 'username')
		self.accountID = cp.get('user', 'accountID')
		self.password = cp.get('user', 'password')
		self.twilioID = cp.get('user', 'twilioID')
		self.twilioToken = cp.get('user', 'twilioToken')
		self.phNumber_from = cp.get('user', 'phNumber_from')
		self.phNumber_to = cp.get('user', 'phNumber_to')
		self.target_subject = cp.get('user', 'target_subject')


	def detail(self):

		print 'Hi,', self.username, '-', self.accountID, '.'
		print 'The subject to be found is:', self.target_subject
		print 'The alert message will be sent from:', self.phNumber_from, 'to:', self.phNumber_to, 'immediately once its found!'




