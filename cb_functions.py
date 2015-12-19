import random
CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"

def REQ_ENGINE_ASSEMBLED(master, task, game_state):
        print("REQ_ENGINE_ASSEMBLED")
        return True

def AC_ADD_4_BATTARIES_TASKS(master, task, game_state):
        game_state.add_active_task_with_id(1)


def REQ_CHECK_BATTARIES(master, task, game_state):
        print("REQ_CHECK_BATTARIES")
        return True

def AC_PRESS_HERABORA(master, task, game_state):
        game_state.add_active_task_with_id(2)

def REQ_CHECK_HERABORA(master, task, game_state):
        heraboraPressed = master.getButtons(CB_SLAVE_2).get()[12]
        print("Herabora value: {}\n", heraboraPressed)
        return heraboraPressed

def AC_CB_ADD_RANDOM_TASK(master, task, game_state):

        avaliableTaskIds = game_state.getAvaliableCBTaskIds()
        print("len avaliableTasksid = {}".format(len(avaliableTaskIds)))
        if len(avaliableTaskIds) == 0:
                return


        # check if task already true - than we don't need execute
        randomTaskRequirement = True
        while randomTaskRequirement:
            randomId = random.randint(0, len(avaliableTaskIds) -1)
            # print("avaliable task with random id {}".format(avaliableTaskIds[randomId]))

            randomTaskId = avaliableTaskIds[randomId]
            randomTask = game_state.find_task_with_id(randomTaskId)
            randomTaskRequirement = randomTask.success_requirements(master, game_state.state, game_state)

        game_state.add_active_task_with_id(randomTaskId)

        game_state.update_used_task_ids_list(randomTaskId)

def AC_ADD_END_GAME_TASK(master, task, game_state):
        game_state.add_active_task_with_id(3)

def REQ_AMOUNT_OF_TASK_SUCCESSED(master, task, game_state):
    if game_state.successfullTasksForWin == game_state.successfullTasksCounter:
            return True
    return False

def AC_ENTERED_DOOR_OPEN(master, task, game_state):
        print("Entered door opened")

def AC_SHOW_SUCCESS_MESSAGE(master, task, game_state):
        print("You are WINNER!")

def REQ_AMOUNT_OF_TASK_FAILURE(master, task, game_state):
        return False

def AC_SHOW_FAILURE_MESSAGE(master, task, game_state):
        print("You lose")


# Tasks

def REQ_CB_TASK_FAILURE(master, task, game_state):
    """ Failure requarement for Captain's bridge tasks """
    return game_state.cbTaskFailure(task)


class Cb1Buttons:
        pass

class Cb2Buttons:
        PRESLO = 0
        KOKOVNIK = 1
        TRUNDEL = 2
        GLUKALO = 3
        HERABORA = 12

class CB_CTRL:
    """Named constant for Captain's Bridge controls"""
    # Controller 1
    # Buttons
    REPULSIVE_DESYNCRONISER = 0
    LEVITRON = 1
    DEFLECTOR = 2
    BIG_RED_BUTTON = 3
    KRIVOSHUP_MINUS = 4
    KRIVOSHUP_PLUS = 5
    SERVO_COOLING_SYSTEM = 6
    # ADC
    # Муфта обратного цикла
    CLUTCH_REVERSE_CYCLE = 1
    SUPER_BRAIN = 0

def REQ_SERVO_COOLING_SYSTEM_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return buttons[CB_CTRL.SERVO_COOLING_SYSTEM]

def REQ_SERVO_COOLING_SYSTEM_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.SERVO_COOLING_SYSTEM]

def REQ_DEFLECTOR_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.DEFLECTOR]

def REQ_DEFLECTOR_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.DEFLECTOR]

def REQ_LEVITRON_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.LEVITRON]

def REQ_LEVITRON_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.LEVITRON]

def REQ_KRIVOSHUP_PLUS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.KRIVOSHUP_PLUS]

def REQ_KRIVOSHUP_PLUS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.KRIVOSHUP_PLUS]

def REQ_KRIVOSHUP_MINUS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.KRIVOSHUP_MINUS]

def REQ_KRIVOSHUP_MINUS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.KRIVOSHUP_MINUS]

def REQ_REPULSIVE_DESYCHRONISER_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.REPULSIVE_DESYNCRONISER]

def REQ_REPULSIVE_DESYCHRONISER_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.REPULSIVE_DESYNCRONISER]

def REQ_BIG_RED_BUTTON_PRESSED(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.BIG_RED_BUTTON]

def REQ_CLUTCH_REVERSE_SYCLE_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 0 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_CLUTCH_REVERSE_SYCLE_TO_77(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 77 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_CLUTCH_REVERSE_SYCLE_TO_150(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 150 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_CLUTCH_REVERSE_SYCLE_TO_255(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 255 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 0 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_255(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 255 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_182(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 182 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_129(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 129 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_86(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 86 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def REQ_SUPER_BRAIN_TO_45(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_1).get()
    return 45 == adc[CB_CTRL.CLUTCH_REVERSE_CYCLE]

def PRESLO_PRESSED(master, task, game_state):
        buttons = master.getButtons(CB_SLAVE_2).get()
        presloPressed = buttons[Cb2Buttons.PRESLO]
        return presloPressed

def KOKOVNIK_PRESSED(master, task, game_state):
        buttons = master.getButtons(CB_SLAVE_2).get()
        kokovnikPressed = buttons[Cb2Buttons.KOKOVNIK]
        return kokovnikPressed

def TRUNDEL_PRESSED(master, task, game_state):
        buttons = master.getButtons(CB_SLAVE_2).get()
        trundelPressed = buttons[Cb2Buttons.TRUNDEL]
        return trundelPressed

def GLUKALO_PRESSED(master, task, game_state):
        buttons = master.getButtons(CB_SLAVE_2).get()
        glukaloPressed = buttons[Cb2Buttons.GLUKALO]
        return glukaloPressed

def HERABORA_PRESSED(master, task, game_state):
        buttons = master.getButtons(CB_SLAVE_2).get()
        glukaloPressed = buttons[Cb2Buttons.HERABORA]
        return glukaloPressed




