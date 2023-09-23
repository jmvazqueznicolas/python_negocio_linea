from mailchimp3 import MailChimp
import os

MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MC_USER = os.getenv('MC_USER')
LIST_ID = os.getenv('LIST_ID')


def get_mailchimp_client():
    return MailChimp(mc_api=MAILCHIMP_API_KEY, mc_user=MC_USER)

def add_subscriber(email):
    client = get_mailchimp_client()
    list_id = LIST_ID
    data = {
        'email_address': email,
        'status': 'subscribed',
    }
    return client.lists.members.create(list_id, data)

    
