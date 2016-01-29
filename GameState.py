# -*- coding: utf-8 -*-
import random
import os
import time
CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"
hallwayPuzzles = "hallwayPuzzles"
def clear():
    os.system('cls' if os.name=='nt' else 'clear')
class CaptainsBridgeController:
    NUM_LEVELS = 5
    NUM_STAGES = 3
    NUM_STAGE_TASKS = 4
    # number all lives for game
    NUM_LIVES = 10

    # time for done stage on level
    PROGRESS_BAR_LEVEL_TIME=[34, 20, 18, 15, 13, 11]

    STAGE_DELAY = 1
    LEVEL_DELAY = 4

    MESSAGE_LEVEL = "Уровень: {level}"
    class LEVEL_MESSAGES:
        LEVEL_1 = "Первичный запрос в сеть"
        LEVEL_2 = "Активация метеоритной защиты"
        LEVEL_3 = "Возобновление подачи топлива"
        LEVEL_4 = "Стабилизация искуственного интеллекта"
        LEVEL_5 = "Активация автопилота"

    class GAME_MESSAGES:
        DOTS = "..."
        SYSTEM_INIT = "...инициализация системы..."
        LOAD_NODES = "...загрузка информационных узлов..."
        RUNNING_APP = "запуск программы..."
        LOGO = "Gen-Ca Inc\nпредставляет"
        PRODUCT_NAME = "Общевидовой пилот без хлопот. v0.78"
        PROG_OPTIMIZATION = "Программа оптимизирует управление судном под ваш(человек) вид"
        GREETINGS = "Привет человеки."
        INSTRUCTIONS = "Управление настроено под (человеки) интеллектуальные способности."
        INSTRUCTIONS_2 = "Чтобы восстановить автопилот - просто нажимайте на кнопки, которые видите на экране"
        PRESS_BUTTON = "Когда будете готовы - жмите H.E.R.A.B.O.R.A"


        FINAL_MESSAGE = "Поздравляю, вы активировали автопилот. Возвращайтесь в криокамеру."

    def __init__(self, game_state):
        self.game_state = game_state
        self.current_level = 0
        self.current_stage = 0
        self.current_lives_num = self.NUM_LIVES
        self.completed_tasks_num = 0
        self.progress_bar_delay = 1
        self.progress_bar_read_time_start = time.time()

    def get_progress_bar_time(self):
        return self.PROGRESS_BAR_LEVEL_TIME[self.current_level]

    def progress_bar_read_state(self):
        current_time = time.time()
        if (current_time - self.progress_bar_read_time_start) > self.progress_bar_delay:
            return True
        return False

    def progress_bar_delay_restart(self):
        self.progress_bar_read_time_start = time.time()

    def task_success(self, task):
        if task.type == 'CB_TASK':
            self.completed_tasks_num = self.completed_tasks_num + 1
            self.showOkMessage(task)
            monitorId = self.game_state.getMonitorIdByTask(task)

    def task_failure(self, task):
        if unicode(task.type) == u'CB_TASK':

            self.current_stage = 1
            self.completed_tasks_num = 0

            self.progressBarReset()
            self.game_state.monitorsWithProgressBarZero = []

            self.remove_random_tasks()

            self.add_random_tasks()


    def remove_random_tasks(self):
        active_cb_task_list = [atask for atask in self.game_state.active_tasks if unicode(atask.type) == u'CB_TASK']
        for someActiveTask in active_cb_task_list:
            self.game_state.remove_active_task(someActiveTask)

    def add_random_tasks(self):
        for index in range(4):
            self.game_state.add_cb_random_task()

    def check(self):
        # Begin
        if self.current_level == 0:
            # use it in quest_full.py
            # self.show_initialization_messages()
            self.current_level = 1
            self.current_stage = 1
            self.showLevelMessage()
            time.sleep(self.LEVEL_DELAY)

            self.add_random_tasks()

        stage_up = False
        level_up = False
        # stage increment
        if self.completed_tasks_num >= self.NUM_STAGE_TASKS:
           self.completed_tasks_num = 0
           self.current_stage = self.current_stage + 1
           stage_up = True
           time.sleep(self.STAGE_DELAY)

        # level increment
        if self.current_stage > self.NUM_STAGES:
            self.current_stage = 1
            self.current_level = self.current_level + 1
            if self.current_level > self.NUM_LEVELS:
                #game end
                self.remove_random_tasks()
                self.show_on_all_monitors(self.GAME_MESSAGES.FINAL_MESSAGE)
                return True

            level_up = True
            self.showLevelMessage()
            time.sleep(self.LEVEL_DELAY)

        # add tasks
        if stage_up or level_up:
            self.add_random_tasks()

        return

    def progressBarReset(self):
        message = ""
        for monitorId in range(1,5):
            self.game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'progress_visible': False})

    def showOkMessage(self, task):

        monitorId = self.game_state.getMonitorIdByTask(task)
        message = "OK"
        self.game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'progress_visible': False})

    def show_on_all_monitors(self, message):
        for monitorId in range(1,5):
            self.game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'progress_visible': False})

    def showLevelMessage(self):
        if self.current_level == 1:
            message = self.LEVEL_MESSAGES.LEVEL_1
        elif self.current_level == 2:
            message = self.LEVEL_MESSAGES.LEVEL_2
        elif self.current_level == 3:
            message = self.LEVEL_MESSAGES.LEVEL_3
        elif self.current_level == 4:
            message = self.LEVEL_MESSAGES.LEVEL_4
        elif self.current_level == 5:
            message = self.LEVEL_MESSAGES.LEVEL_5
        else:
            return

        self.show_on_all_monitors(message)

    def beautiful_type(self, message, wordDelay=0.3):
        half_message = ""
        for word in message:
            half_message = half_message + word
            print("beautiful_type: {}".format(half_message))
            self.show_on_all_monitors(half_message)
            time.sleep(wordDelay)



    def show_initialization_messages(self):

        self.show_on_all_monitors(self.GAME_MESSAGES.DOTS)
        time.sleep(2)
        self.show_on_all_monitors(self.GAME_MESSAGES.SYSTEM_INIT)
        time.sleep(4)
        self.show_on_all_monitors(self.GAME_MESSAGES.LOAD_NODES)
        time.sleep(3)
        self.show_on_all_monitors(self.GAME_MESSAGES.RUNNING_APP)
        time.sleep(3)
        self.show_on_all_monitors(self.GAME_MESSAGES.LOGO)
        time.sleep(4)
        self.show_on_all_monitors(self.GAME_MESSAGES.PRODUCT_NAME)
        time.sleep(4)
        self.show_on_all_monitors(self.GAME_MESSAGES.DOTS)
        time.sleep(2)
        self.show_on_all_monitors(self.GAME_MESSAGES.PROG_OPTIMIZATION)
        time.sleep(3)
        self.show_on_all_monitors(self.GAME_MESSAGES.GREETINGS)
        time.sleep(4)
        self.show_on_all_monitors(self.GAME_MESSAGES.INSTRUCTIONS)
        time.sleep(4)
        self.show_on_all_monitors(self.GAME_MESSAGES.INSTRUCTIONS_2)
        time.sleep(4)
        self.show_on_all_monitors(self.GAME_MESSAGES.INSTRUCTIONS_2)
        time.sleep(3)
        self.show_on_all_monitors(self.GAME_MESSAGES.DOTS)
        time.sleep(1)
        self.show_on_all_monitors(self.GAME_MESSAGES.PRESS_BUTTON)


        pass



class GameState:
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
        self.failureTasksForLose = 5
        self.successfullTasksCounter = 0
        self.failureTasksCounter = 0

        self.cb_controller = CaptainsBridgeController(self)

        # tasks whom been active on previously steps
        # it's fill in add_random_tasks
        self.usedTasksIds = []
        self.numUsedTasks = 22

        # always allow to open enter door
        self.openDoorPermission = [True, False, False]

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
        message = {'message': [x.title for x in self.active_tasks]}
        callback(message) if callback else None


    def perform_task_if_satisfies(self, task):
        # if task.success_requirements_satisfied(self.device_master, task, self):
        if task.success_requirements_satisfied(self.device_master, task, self):
            # counter inc only if task is Captain's Bridge type
            self.incSuccessfullTaskCounter(task)
            self.cb_controller.task_success(task)

            self.remove_active_task(task)
            task.perform_success_actions(self.device_master, task, self)

        elif task.failure_requirements_satisfied(self.device_master, task, self):
            # remove task from active list
            # remove task from monitor list
            # remove monitor from Progress bar zero list
            # monitor removed in cbTaskFailure
            self.incFailureTaskCounter(task)
            self.cb_controller.task_failure(task)
            self.remove_active_task(task)
            # Increment failure tasks counter
            # if task is Captian's bridge
            task.perform_failure_actions(self.device_master, task, self)



    def add_task(self, task):
        self.tasks.append(task)

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

    def incFailureTaskCounter(self, task):
        if unicode(task.type) == u'CB_TASK':
            self.failureTasksCounter = self.failureTasksCounter + 1

    def incSuccessfullTaskCounter(self, task):
        if unicode(task.type) == u'CB_TASK':
            self.successfullTasksCounter = self.successfullTasksCounter + 1

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
