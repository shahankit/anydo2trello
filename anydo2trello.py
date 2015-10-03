"""
Created on 5 May 2015

@author: shahankit
"""
import sys
from anydo.api import AnyDoAPI
from CreateOnTrello import CreateOnTrello

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
task_dict = {}
for task in tasks:
	task_dict[task['id']] = task

for task in tasks:
	if task.get('parentGlobalTaskId'):
		poped_task = task_dict.pop(task['id'])
		task_dict[task['parentGlobalTaskId']]['subTasks'].append(task)

for key in task_dict:
	task = {'title':task_dict[key]['title'], 'sub_tasks':[], 'status':task_dict[key]['status'], 'desc':task_dict[key].get('note','')}
	for sub_task in task_dict[key]['subTasks']:
		task['sub_tasks'].append({'title':sub_task['title'], 'status':sub_task['status']})
	category_data[task_dict[key]['categoryId']]['tasks'].append(task)

api_key = '4d9fc7d42300c24218a2eafabd76f5f8'

client = CreateOnTrello(api_key = api_key, application_name = 'anydo2trello', token_expires = '1day')
auth_token = raw_input('Enter you auth token here: ')
client = CreateOnTrello(api_key = api_key, application_name = 'anydo2trello', token_expires = '1day', auth_token = auth_token)

for category in category_data:
	print category_data[category]['name']
	board = client.create_board(category_data[category]['name'])
	completed_list = client.create_list('Done', board)		#Move checked cards to Done list
	incomplete_list = client.create_list('To Do', board)	#Mode unchecked cards to To Do list
	category_tasks = category_data[category]['tasks']
	for task in category_tasks:
		print '\t'+task['title']
		if task['status'] == 'CHECKED':
			card = client.create_card(task['title'], completed_list, task['desc'])
		else:
			card = client.create_card(task['title'], incomplete_list, task['desc'])
		if len(task['sub_tasks']) > 0:
			checklist = client.create_checklist(card, 'Sub tasks')
		for sub_task in task['sub_tasks']:
			print '\t\t'+sub_task['title']
			if sub_task['status'] == 'CHECKED':
				checkitem = client.create_checkitem(checklist, sub_task['title'], 1)
			else:
				checkitem = client.create_checkitem(checklist, sub_task['title'], 0)
