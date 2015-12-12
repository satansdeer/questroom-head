# -*- coding: utf-8 -*-
class GameState:
    startCBTaskId = 6
    numCBTasks = 6
    def __init__(self):
        self.device_master = None
        self.tasks = []
        self.active_tasks = []
        self.state = {'pressed_buttons':[]}


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
            self.active_tasks.remove(task)
            print("---- %s" % task.title)
        elif task.failure_requirements_satisfied(self.device_master, self.state, self):
            task.perform_failure_actions(self.device_master, self.state, self)
            self.active_tasks.remove(task)



    def add_task(self, task):
        self.tasks.append(task)


    def add_active_task_with_id(self, id):
        task = self.find_task_with_id(id)
        self.quest_room.send_ws_message(1, {'message':task.title})
        self.active_tasks.append(task)


    def find_task_with_id(self, id):
        for task in self.tasks:
            if int(task.id) == int(id):
                return task

    #def getAvaliableCBTaskIds():
	#allCBTask = self.task[startCBTaskId:numCBTasks] 
        #[x for x in y if x ]	

    	#return avaliableTaskIds

    def apply_state(self, state):
        pass
