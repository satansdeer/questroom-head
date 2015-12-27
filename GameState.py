# -*- coding: utf-8 -*-
import random
import os
CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"
hallwayPuzzles = "hallwayPuzzles"
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
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

        # whis list used by failure requarements of CB tasks
        self.monitorsWithProgressBarZero = []
        # successfull and failure taks counters
        self.successfullTasksForWin = 10
        self.failureTasksForLose = 10
        self.successfullTasksCounter = 0
        self.failureTasksCounter = 0

        # tasks whom been active on previously steps
        # it's fill in add_random_tasks
        self.usedTasksIds = []
        self.numUsedTasks = 12

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
        # print("active tasks list:{}".format(self.active_tasks))
        # print("Active Tasks:{}".format([tas__k.id for tas__k in self.active_tasks]))
        for task in self.active_tasks:
            # print("Active Tasks:{}".format([tas__k.id for tas__k in self.active_tasks]))
            # print("TAsi to perform satisfies: {id}, {obj}".format(id=task.id, obj=task))
            self.perform_task_if_satisfies(task)
        message = {'message': self.active_tasks}
        callback(message) if callback else None
       # os.system('cls' if os.name=='nt' else 'clear')
       # print("CB_SLAVE_1")
       # self.device_master.getButtons(CB_SLAVE_1).printResource()
       # self.device_master.getAdc(CB_SLAVE_1).printResource()
       # print("CB_SLAVE_2")
       # self.device_master.getButtons(CB_SLAVE_2).printResource()
       # self.device_master.getAdc(CB_SLAVE_2).printResource()


    def perform_task_if_satisfies(self, task):
        # print("TAsk in perform satisfies: {id}, {obj}".format(id=task.id, obj=task))
        if task.success_requirements_satisfied(self.device_master, self.state, self):
            self.remove_active_task(task)
            # counter inc only if task is Captain's Bridge type
            self.incSuccessfullTaskCounter(task)

            # print("After remove action")
            # print("Active task name: {}".format([taskm.title for taskm in  self.active_tasks]))
            # print("Active task id: {}".format([taskm.id for taskm in  self.active_tasks]))
            # print("All task id: {}".format([taskm.id for taskm in  self.tasks]))

            task.perform_success_actions(self.device_master, self.state, self)
            # print("---- %s" % task.title)

        elif task.failure_requirements_satisfied(self.device_master, self.state, self):
            # remove task from active list
            # remove task from monitor list
            # remove monitor from Progress bar zero list
            # monitor removed in cbTaskFailure 
            self.remove_active_task(task)
            # Increment failure tasks counter
            # if task is Captian's bridge
            self.incFailureTaskCounter(task)
            task.perform_failure_actions(self.device_master, self.state, self)



    def add_task(self, task):
        self.tasks.append(task)

    def remove_active_task(self, task):
        print("Remove task with id: {}".format(task.id))
        if task.showOnMonitor:
                self.freeMonitor(task)
                print("Free monitor with id {}".format(task.id))
        if task in self.active_tasks:
            self.active_tasks.remove(task)

    def add_active_task_with_id(self, id):
        print("Task id for add: {}".format(id))
        task = self.find_task_with_id(id)
        if task.showOnMonitor:
                monitorId = self.fillMonitor(task)
                print("Add active Task id: {taskId} | monitorId: {monitorId}\n".format(taskId=id, monitorId=monitorId))
                self.quest_room.send_ws_message(str(monitorId), {'message':task.title})
        print("self.active_tasks.append task: {}".format(task.id))
        self.active_tasks.append(task)
        print("ADD: active_tasks: {}".format([task_.id for task_ in self.active_tasks]))

    def update_used_task_ids_list(self, taskId):
        self.usedTasksIds.insert(0, taskId) 
        if len(self.usedTasksIds) > self.numUsedTasks:
            self.usedTask.pop()

    # def cbTaskType(self, task):
    #     # if self.startCBTaskId <= int(task.id) <= (self.startCBTaskId + self.numCBTasks):
    #     print("Task id {}, task type: {}".format(task.id, task.type))
    #     if task.type == 'CB_TASK':
    #             print("It's CB task!!!")
    #             return True
    #     return False

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

    def getMonitorIdByTask(self, task):
        taskId = task.id
        for monitor in self.monitors:
           if monitor['task'] == taskId:
               return monitor['id']
        return None

    def incFailureTaskCounter(self, task):
        if task.type == 'CB_TASK':
            self.failureTasksCounter = self.failureTasksCounter + 1

    def incSuccessfullTaskCounter(self, task):
        if task.type == 'CB_TASK':
            self.successfullTasksCounter = self.successfullTasksCounter + 1

    def cbTaskFailure(self,task):
        """Checked is progress bar for task is zero
            Using only by Captain's bridge tasks"""
        monitorId = self.getMonitorIdByTask(task)
        if monitorId in self.monitorsWithProgressBarZero:
            self.monitorsWithProgressBarZero.remove(monitorId)
            return True
        return False

    def find_task_with_id(self, id):
        for task in self.tasks:
            if int(task.id) == int(id):
                return task


    def getAvaliableCBTaskIds(self):
        # get  only CaptainBridge Tasks
        allCBTasksIds = [task.id for task in self.tasks if self.cbTaskType(task)]
        print("AllCBTask: {}".format(allCBTasksIds))
        # get id not active tasks and not used recently
        avaliableTasksIds = [taskId for taskId in allCBTasksIds if taskId not in self.usedTasksIds]
        print('Avaliable task Ids: {}'.format(avaliableTasksIds))

        return avaliableTasksIds

    def cbTaskType(self, task):
        print("Task id {}, task type: {}".format(task.id, task.type))
        return str(task.type) == "CB_TASK"

    def apply_state(self, state):
        pass


    def updateMonitorsListWithProgressBarZero(self,monitorId):
        """append monitor number in list of monitors with zero ProgressBar """
        if monitorId in self.monitorsWithProgressBarZero:
            return
        self.monitorsWithProgressBarZero.append(monitorId)
