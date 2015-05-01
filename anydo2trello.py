import sys
from anydo.api import AnyDoAPI

anydo_username = raw_input('Enter username for any.do : ')
anydo_password = raw_input('Enter password for any.do : ')

api = AnyDoAPI(username = anydo_username, password = anydo_password)

try:
    api.get_user_info()
except:
	print ('Invalid username or password')
	sys.exit(1)

categories = api.get_all_categories()
category_data = {}
for category in categories:
    category_data[category['id']] = {'name':category['name'], 'tasks':[]}

tasks = api.get_all_tasks()