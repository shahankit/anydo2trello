"""
Created on 5 May 2015

@author: shahankit
"""
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
category_ids = {}
for category in categories:
    category_data[category['id']] = {'name':category['name'], 'tasks':[]}
    category_ids[category['id']] = []

tasks = api.get_all_tasks()
for task in tasks:
	category_ids[task['categoryId']].append(task['id'])

for key in category_ids:
	print ('In category :'+category_data[key]['name'])
	for task_id in category_ids[key]:
		category_ids[key].remove(task_id)
		task = api.get_task_by_id(task_id)
		print ('\tScanning task : '+task['title'])
		category_data[key]['tasks'].append(task)
		for sub_task in task['subTasks']:
			category_data[key].pop(sub_task['id'], None)
			try:
				category_ids[key].remove(sub_task['id'])
			except ValueError:
				pass
