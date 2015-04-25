"""
Created on 25 Apr 2015

@author: shahankit
"""

from trolly.client import Client
from trolly.member import Member
from trolly.list import List
from trolly.board import Board
from trolly.card import Card
from trolly.authorise import Authorise

if __name__ == '__main__':
	
	import sys

	option = ''

	try:
		option = sys.argv[1]
		api_key = sys.argv[2]
		application_name = sys.argv[3]

		if len(sys.argv) >= 5:
			token_expires = sys.argv[4]

		else:
			token_expires = '1day'

	except:
		pass

	if option == '-a':
		auth = Authorise(api_key)
		authURL = auth.get_authorisation_url(application_name, token_expires)
		print authURL
