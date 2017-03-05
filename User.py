class User:
	
	username = '<your name>'
	accountID = '<your student ID>'
	password = '<your password>'

	twilioID = '<your twilio account id>'
	twilioToken = '<your twilio token>'

	phNumber_from = '<your twilio phone number>'
	phNumber_to = '<your own phone number>'

	target_subject = '<subject number> - <subject full name>'

	def detail(self):
		print 'Hi,', self.username, '-', self.accountID, '.'
		print 'The subject to be found is:', self.target_subject
		print 'The alert message will be sent from:', self.phNumber_from, 'to:', self.phNumber_to, 'immediately once its found!'



