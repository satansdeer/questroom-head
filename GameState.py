# -*- coding: utf-8 -*-
import random
import os
import time
import datetime
import copy

from CaptainsBridgeController import CaptainsBridgeController

CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"
hallwayPuzzles = "hallwayPuzzles"
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

class GameState:
    def __init__(self):
        self.device_master = None
        self.tasks = []

        self.active_tasks = []
        self.active_tasks_old_state = []

        self.skipped_tasks = [];

        self.state = {'pressed_buttons':[]}

        self.monitors = [ { 'id': 1, 'task': None },
                          { 'id': 2, 'task': None },
                          { 'id': 3, 'task': None },
                          { 'id': 4, 'task': None },
                        ]

        # whis list used by failure requarements of CB tasks
        self.monitorsWithProgressBarZero = []

        self.cb_controller = CaptainsBridgeController(self)

        # tasks whom been active on previously steps
        # it's fill in add_random_tasks
        self.usedTasksIds = []
        self.numUsedTasks = 22

        # always allow to open enter door
        self.openDoorPermission = [True, False, False]

        self.send_time_to_monitors = True

        self.time_stamp_old = time.time()
        self.time_stamp_new = time.time()

        self.time_stamp_to_send = time.time()

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

        if self.active_tasks_old_state != self.active_tasks:
            self.active_tasks_old_state = copy.copy(self.active_tasks)
            callback(None) if callback else None

        if self.send_time_to_monitors:
            self.time_stamp_new = time.time()
            secondLeft = (self.time_stamp_new - self.time_stamp_old) > 1
            if secondLeft:
                self.time_stamp_old = time.time()
                time_string = datetime.datetime.now().strftime("%H:%M:%S")
                # print("Send time to monitors: {}".format(time_string))
                for monitorId in range(1,5):
                    self.quest_room.send_ws_message(str(monitorId), {'message': time_string , 'progress_visible': False, 'not_a_task': True})


    def perform_task_if_satisfies(self, task):

        task_success = task.success_requirements_satisfied(self.device_master, task, self)

        task_skipped = task in self.skipped_tasks
        if task_skipped:
            print("Task with id {}: skipped".format(task.id))
            self.skipped_tasks.remove(task)

        if task_success or task_skipped:

            self.cb_controller.task_success(task)

            self.remove_active_task(task)

            task.perform_success_actions(self.device_master, task, self)

        elif task.failure_requirements_satisfied(self.device_master, task, self):

            self.cb_controller.task_failure(task)

            self.remove_active_task(task)

            task.perform_failure_actions(self.device_master, task, self)



    def add_task(self, task):
        self.tasks.append(task)

    def task_with_id_active(self, task_id):
        for active_task in self.active_tasks:
            if active_task.id == task_id:
                return True
        return False

    def remove_active_task(self, task):
        if task.showOnMonitor:
            self.freeMonitor(task)
        if task in self.active_tasks:
            self.active_tasks.remove(task)

    def add_cb_random_task(self):

        avaliableTaskIds = self.getAvaliableCBTaskIds()
        if len(avaliableTaskIds) == 0:
                return

        # check if task already true - than we don't need execute
        randomTaskRequirement = True
        # reinit pseudo generator
        random.seed()
        while randomTaskRequirement:
            randomId = random.randint(0, len(avaliableTaskIds) -1)

            randomTaskId = avaliableTaskIds[randomId]
            randomTask = self.find_task_with_id(randomTaskId)
            randomTaskRequirement = randomTask.success_requirements_satisfied(self.device_master, randomTask, self)

        self.add_active_task_with_id(randomTaskId)
        self.update_used_task_ids_list(randomTaskId)

    def add_active_task_with_id(self, id):
        task = self.find_task_with_id(id)
        if task.showOnMonitor:
                monitorId = self.fillMonitor(task)
                progress_bar_time = self.cb_controller.get_progress_bar_time()
                current_level = self.cb_controller.current_level
                current_stage = self.cb_controller.current_stage
                self.quest_room.send_ws_message(str(monitorId), {'message':task.title, 'progress_bar_time': progress_bar_time, 'level': current_level, 'stage': current_stage})
        self.active_tasks.append(task)

    def update_used_task_ids_list(self, taskId):
        self.usedTasksIds.insert(0, taskId)
        if len(self.usedTasksIds) > self.numUsedTasks:
            self.usedTasksIds.pop()

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

    def cbTaskFailure(self,task):
        """Checked is progress bar for task is zero
            Using only by Captain's bridge tasks"""
        monitorId = self.getMonitorIdByTask(task)
        if monitorId in self.monitorsWithProgressBarZero:
            return True
        return False

    def find_task_with_id(self, id):
        for task in self.tasks:
            if int(task.id) == int(id):
                return task


    def getAvaliableCBTaskIds(self):
        # get  only CaptainBridge Tasks
        allCBTasksIds = [task.id for task in self.tasks if self.cbTaskType(task)]
        # get id not active tasks and not used recently
        avaliableTasksIds = [taskId for taskId in allCBTasksIds if taskId not in self.usedTasksIds]

        return avaliableTasksIds

    def cbTaskType(self, task):
        #print("Task id {}, task type: {}".format(task.id, task.type))
        return unicode(task.type) == u'CB_TASK'

    def apply_state(self, state):
        pass


    def updateMonitorsListWithProgressBarZero(self,monitorIdStr):
        """append monitor number in list of monitors with zero ProgressBar """
        if self.cb_controller.progress_bar_read_state():
            self.cb_controller.progress_bar_delay_restart()

            monitorId = int(monitorIdStr)

            if monitorId in self.monitorsWithProgressBarZero or len(self.monitorsWithProgressBarZero) != 0:
                return
            self.monitorsWithProgressBarZero.append(monitorId)


    def allowOpenDoor(self, doorNumber):
        if 0 <= doorNumber < len(self.openDoorPermission):
            self.openDoorPermission[doorNumber] = True

    def canOpenDoor(self, doorNumber):
        if 0 <= doorNumber < len(self.openDoorPermission):
            return self.openDoorPermission[doorNumber]
        return False
