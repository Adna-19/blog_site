from django.conf import settings
import hashlib
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

def setup_configurations():
	mailchimp = Client()
	mailchimp.set_config({
		"api_key": settings.MAILCHIMP_API_KEY,
		"server": settings.MAILCHIMP_DATA_CENTER
	})
	return mailchimp

def subscribe(email):
	mailchimp = setup_configurations()
	member_info = {
		'email_address': email,
		'status': 'subscribed',
	}

	try:
		response = mailchimp.lists.add_list_member(
			settings.MAILCHIMP_EMAIL_LIST_ID,
			member_info
		)
	except ApiClientError as error:
		print(f"An exception occurred : {error.text}")

def unsubscribe(member_email):
	mailchimp = setup_configurations()
	member_email_hash = hashlib.md5(member_email.encode('utf-8')).hexdigest()
	member_update = {'status': 'unsubscribed'}

	try:
		response = mailchimp.lists.update_list_member(
			settings.MAILCHIMP_EMAIL_LIST_ID,
			member_email_hash,
			member_update
		)
	except ApiClientError as error:
		print(f"An exception occurred: {error.text}")