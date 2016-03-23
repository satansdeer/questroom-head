# -*- coding: utf-8 -*-
import time

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
        RUNNING_APP = "...запуск программы..."
        LOGO = "Gen-Ca Inc\nпредставляет"
        PRODUCT_NAME = "Общевидовой пилот без хлопот. v0.78"
        PROG_OPTIMIZATION = "Программа оптимизирует управление судном под ваш(человек) вид"
        GREETINGS = "Привет человеки."
        INSTRUCTIONS = "Управление настроено под (человеки) интеллектуальные способности."
        INSTRUCTIONS_2 = "Чтобы восстановить автопилот - просто нажимайте на кнопки, которые видите на экране"
        PRESS_BUTTON = "Когда будете готовы - жмите H.E.R.A.B.O.R.A"


        FINAL_MESSAGE = "Поздравляю, вы активировали автопилот. Возвращайтесь в криокамеру.\nДля поднятия боевого духа играет бодрящая музыка"

    def __init__(self, game_state):
        self.game_state = game_state
        self.initialization()


    def initialization(self):
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
            self.game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'level': self.current_level, 'progress_visible': False})

    def showOkMessage(self, task):
        monitorId = self.game_state.getMonitorIdByTask(task)
        message = "OK"
        self.game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'level': self.current_level, 'progress_visible': False, 'not_a_task': True})

    def show_on_all_monitors(self, message):
        for monitorId in range(1,5):
            self.game_state.quest_room.send_ws_message(str(monitorId), {'message': message, 'level': self.current_level, 'progress_visible': False, 'not_a_task': True})

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



