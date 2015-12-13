# -*- coding: utf-8 -*-
import random
class GameState:
    startCBTaskId = 6
    numCBTasks = 6
    def __init__(self):
        self.device_master = None
        self.tasks = []
        self.active_tasks = []
        self.state = {'pressed_buttons':[]}

	self.monitors = [ { 'id': 1, 'task': None },
			  { 'id': 2, 'task': None },
			  { 'id': 3, 'task': None },
			  { 'id': 4, 'task': None },
			]

    def start_game_loop(self, callback):
        if not self.device_master: return
        if not self.slave: return

        root_task = self.find_task_with_id(0)
        self.active_tasks.append(root_task)
        while len(self.active_tasks):
            self.game_loop(callback)
            self.state['pressed_buttons'] = []


    def game_loop(self, callback):
        if not self.state: return
        for task in self.active_tasks:
            self.perform_task_if_satisfies(task)
        #callback(message) if callback else None


    def perform_task_if_satisfies(self, task):
        if task.success_requirements_satisfied(self.device_master, self.state, self):
            self.remove_active_task(task)
	    print("After remove action")
	    print("Active task name: {}".format([taskm.title for taskm in  self.active_tasks]))
	    print("Active task id: {}".format([taskm.id for taskm in  self.active_tasks]))
	    print("All task id: {}".format([taskm.id for taskm in  self.tasks]))
            task.perform_success_actions(self.device_master, self.state, self)
            print("---- %s" % task.title)
        elif task.failure_requirements_satisfied(self.device_master, self.state, self):
            self.remove_active_task(task)
            task.perform_failure_actions(self.device_master, self.state, self)



    def add_task(self, task):
        self.tasks.append(task)

    def remove_active_task(self, task):
    	print("Remove task with id: {}".format(task.id))
	if task.showOnMonitor:
		self.freeMonitor(task)
		print("Free monitor with id {}".format(task.id))
	self.active_tasks.remove(task)	

    def add_active_task_with_id(self, id):
        task = self.find_task_with_id(id)
	if task.showOnMonitor:
		monitorId = self.fillMonitor(task)
		print("Add active Task id: {taskId} | monitorId: {monitorId}\n".format(taskId=id, monitorId=monitorId))
        	self.quest_room.send_ws_message(str(monitorId), {'message':task.title})
        print("self.active_tasks.append task: {}".format(task.id))
	self.active_tasks.append(task)


    def cbTaskType(self, task):
	if self.startCBTaskId <= int(task.id) <= (self.startCBTaskId + self.numCBTasks):
		return True
	return False
    def freeMonitor(self, task):
	for monitor in self.monitors:
		if monitor['task'] == task.id:
			monitor['task'] = None
			return monitor['id']

    def fillMonitor(self, task):
	for monitor in self.monitors:
		if monitor['task'] is None:
			monitor['task'] = task.id
			return monitor['id']

    def find_task_with_id(self, id):
        for task in self.tasks:
            if int(task.id) == int(id):
                return task

    def getAvaliableCBTaskIds(self):
	# get  only CaptainBridge Tasks
	allCBTask = [self.find_task_with_id(6), self.find_task_with_id(7), self.find_task_with_id(8), self.find_task_with_id(9), self.find_task_with_id(10) ]
	#allCBTask = self.tasks[self.startCBTaskId:self.numCBTasks] 

	# get id not active tasks only
        avaliableTaskIds = [task.id for task in allCBTask if task not in self.active_tasks]	

	print('Avaliable task Ids: {}'.format(avaliableTaskIds))

    	return avaliableTaskIds

    def apply_state(self, state):
        pass
