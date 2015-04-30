"""
Created on 25 Apr 2015

@author: shahankit
"""

from trolly.client import Client
from trolly.member import Member
from trolly.authorise import Authorise
from trolly.trelloobject import TrelloObject

class CreateOnTrello(object):
	"""
	This class contains all the methods which uses the trello API
	to get authorisation url for user and create board, list, card 
	and comment.
	"""
	def __init__(self, api_key, application_name, token_expires='1day', auth_token=None):
		super(CreateOnTrello, self).__init__()
		if (auth_token is None):
			self.api_key = api_key
			auth = Authorise(api_key)
			auth.get_authorisation_url(application_name, token_expires)
			return 'unauthorized'
		else
			self.api_key = api_key
			self.create_user(auth_token)
			return 'authorized'
	
	def create_user(self, user_auth_token):
		"""
		Initiates trello client for the user and also stores list of
		open boards for the user and stores locally as instance variable.
		"""
		self.trello_client = Client(self.api_key, user_auth_token)
		member = Member(self.trello_client, 'me')
		self.get_open_boards(member)

	def get_open_boards(self, member):
		"""
		Get all the open baords for the user.
		"""
		if not hasattr(self, 'boards'):
			boards = member.get_boards()
			open_list = []
			for board in boards:
				info = board.get_board_information({'fields':'closed'})
				if not info['closed']:
					open_list.append(board)
			self.boards = open_list
		return self.boards

	def create_board(self, board_name):
		"""
		Creates a new board with name board_name. If an open board with 
		same name already exists it returns a board object of existing 
		board else creates a new board and returns a board object for 
		new board.
		"""
		open_boards = self.get_open_boards(Member(self.trello_client, 'me'))
		for board in open_boards:
			if board.name == board_name:
				return board

		boards_json = self.trello_client.fetch_json(
			uri_path='/boards', 
			http_method='POST', 
			query_params={'name':board_name}
		)
		return self.trello_client.create_board(boards_json)

	def create_list(self, list_name, board):
		lists_list = board.get_lists()
		for board_list in lists_list:
			if board_list.name == list_name:
				return board_list
		return board.create_list({'name':list_name})

	def create_card(self, card_title, trello_list, desc=None):
		trello_list.add_card({'name':card_title, 'desc':desc, 'date':None})
