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
for category in categories:
    category_data[category['id']] = {'name':category['name'], 'tasks':[]}

tasks = api.get_all_tasks()
task_dict = {}
for task in tasks:
	task_dict[task['id']] = task

for task in tasks:
	if task.get('parentGlobalTaskId'):
		task_dict.pop(task['id'])
		task_dict[task['parentGlobalTaskId']]['subTasks'].append(task)

for key in task_dict:
	task = {'title':task_dict[key]['title'], 'sub_tasks':[], 'status':task_dict[key]['status'], 'desc':task_dict[key].get('note','')}
	for sub_task in task_dict[key]['subTasks']:
		task['sub_tasks'].append({'title':sub_task['title'], 'status':sub_task['status']})
	category_data[task_dict[key]['categoryId']]['tasks'].append(task)
