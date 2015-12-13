# -*- coding: utf-8 -*-
class GameState:
    startCBTaskId = 6
    numCBTasks = 6
    def __init__(self):
        self.device_master = None
        self.tasks = []
        self.active_tasks = []
        self.state = {'pressed_buttons':[]}

	self.monitors = [ { 'id': 0, 'task': None }
			  { 'id': 1, 'task': None }
			  { 'id': 2, 'task': None }
			  { 'id': 3, 'task': None }
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
            task.perform_success_actions(self.device_master, self.state, self)
            self.remove_active_task(task)
            print("---- %s" % task.title)
        elif task.failure_requirements_satisfied(self.device_master, self.state, self):
            task.perform_failure_actions(self.device_master, self.state, self)
            self.remove_active_task(task)



    def add_task(self, task):
        self.tasks.append(task)

    def remove_active_task(self, task):
	self.freeMonitor(task)
	self.active_tasks.remove(task)	

    def add_active_task_with_id(self, id):
        task = self.find_task_with_id(id)
	monitorId = self.fillMonitor(task)
        self.quest_room.send_ws_message(monitorId, {'message':task.title})
        self.active_tasks.append(task)


    def cbTaskType(self, task):
	if startCBTaskId <= int(task.id) <= (startCBTaskId + numCBTasks):
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
			return

    def find_task_with_id(self, id):
        for task in self.tasks:
            if int(task.id) == int(id):
                return task

    def getAvaliableCBTaskIds():
	# get  only CaptainBridge Tasks
	allCBTask = self.task[startCBTaskId:numCBTasks] 
	# get id not active tasks only
        avaliableTaskIds = [task.id for task in allCBTask if task not in self.active_tasks]	

	print('Avaliable task Ids: {ids}'.format(avaliableTaskIds))

    	return avaliableTaskIds

    def apply_state(self, state):
        pass
