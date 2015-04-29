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

class CreateOnTrello(object):
	"""
	This class contains all the methods which uses the trello API
	to get authorisation url for user and create board, list, card 
	and comment.
	"""
	def __init__(self, api_key, application_name, token_expires='1day'):
		super(CreateOnTrello, self).__init__()
		self.api_key = api_key
		auth = Authorise(api_key)
		authURL = auth.get_authorisation_url(application_name, token_expires)
	
	def create_user(self, user_auth_token):
		self.trello_client = Client(self.api_key, user_auth_token)
		self.member = Member(self.trello_client, 'me')
		self.member.get_boards()

	def get_open_boards(self):
		if not hasattr(self, 'boards'):
			boards = self.member.get_boards()
			open_list = []
			for board in boards:
				info = board.get_board_information({'fields':'closed'})
				if not info['closed']:
					open_list.append(board)
			self.boards = open_list
		return self.boards

	def create_board(self, board_name):
		open_boards = self.get_open_boards()
		for board in open_boards:
			if board.name == board_name:
				return board


if __name__ == '__main__':
	
	import sys

	option = ''

	try:
		option = sys.argv[1]
		api_key = sys.argv[2]

	except:
		pass

	if option == '-a':
		c = CreateOnTrello(api_key, 'anydo2trello', 'never')
		user_auth_token = raw_input('Enter the generated authorization token here : ')
		c.create_user(user_auth_token)
		c.create_board('testing board')
		boards = c.get_open_boards()
		for board in boards:
			print (board.name)
