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
	to get authorisation url for user and create board, list, card, 
	checklists.
	"""
	def __init__(self, api_key, application_name, token_expires='1day', auth_token=None):
		"""
		If the auth_token is NoneType then generates a url to fetch 
		token, otherwise creates user client.
		"""
		super(CreateOnTrello, self).__init__()
		self.api_key = api_key
		if (auth_token is None):
			auth = Authorise(api_key)
			auth.get_authorisation_url(application_name, token_expires)
		else:
			self.create_user(auth_token)
	
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
		trello_board else creates a new board and returns a trello_board 
		object for new board.
		"""
		member = Member(self.trello_client, 'me')
		open_boards = self.get_open_boards(member)
		for board in open_boards:
			if board.name == board_name:
				return board
		return member.create_new_board({'name':board_name})

	def create_list(self, list_name, trello_board):
		"""
		Creates a new list for the trello_board object in parameters. 
		If a list with similar name already exists returns the existing 
		trello_list, otherwise returns a newly created trello_list.
		"""
		lists_list = board.get_lists()
		for board_list in lists_list:
			if board_list.name == list_name:
				return board_list
		return board.create_list({'name':list_name})

	def create_card(self, card_title, trello_list, desc=None):
		"""
		Create a new card for given trello_list in parameters and returns
		a new trello_card object.
		"""
		return trello_list.add_card({'name':card_title, 'desc':desc, 'date':None})

	def create_checklist(self, trello_card, checklist_title=None):
		"""
		Adds a checklist to trello_card in parameters. Returns a new 
		trello_checklist object.
		"""
		trello_card.add_checklists({'name':checklist_title, 'value':None})
	
	def create_checkitem(self, trello_checklist, checkitem_name, checked=False):
		"""
		Adds a new checkitem to trello_checklist in parameters.
		"""
		trello_checklist.add_item({'name':checkitem_name, 'checked':checked})
