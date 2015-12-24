import random
CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"
hallwayPuzzles = "hallwayPuzzles"

class ButtonsIdTable:
    WIRE_CONNECTION = 11
    FUSE = 6
    MECHANICS_CARD = 10
    ROBOT_HEAD = 8
    ENGINE = 9
    COMMUTATOR = 7

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
    #    # Buttons
    REPULSIVE_DESYNCRONISER = 0
    LEVITRON = 1
    DEFLECTOR = 2
    BIG_RED_BUTTON = 3
    KRIVOSHUP_MINUS = 4
    KRIVOSHUP_PLUS = 5
    SERVO_COOLING_SYSTEM = 6
    ULTRAFOTON = 11
    REPAIR_NANOROBOTS = 12
    C3PO = 14
    R2D2 = 15
    TETRAGEKS = 16
    #    # ADC
    CLUTCH_REVERSE_CYCLE = 1
    SUPER_BRAIN = 0

    # Controller 2
    #    # Buttons
    TPBACH_1 = 0
    TPBACH_2 = 1
    DVORNIKI = 2
    ECO_LAZER = 3

    BATTERY_1 = 7
    BATTERY_2 = 8
    BATTERY_3 = 10
    BATTERY_4 = 6

    PROTON_LAUNCHERS_BATTERY = 4
    DARK_MATTER_STABILIZER = 5
    HERABORA = 12

    #    # ADC
    CHAMAEMELUM_NOBILE = 0
    DIPSOMANIA_SUPERCHARGER = 1
    HYPER_DRIVE_GENERATOR = 2
    CONDENSER = 6

class MESSAGE:
    BATTERY_AVALIABLE = "Battery {id} is inserted"
    BATTERY_ABSENT = "ERROR: Battery {id} missing!"
    ENGINE_BROKEN = "Repair engine"
    PRESS_HERABORA = "When you're ready press HERABORA"

def REQ_ENGINE_ASSEMBLED(master, task, game_state):
    buttons = master.getButtons(hallwayPuzzles).get()
    engine = buttons[ButtonsIdTable.ENGINE]
    return engine

def AC_SHOW_ENGINE_MESSAGE(master, task, game_state):
    if REQ_ENGINE_ASSEMBLED(master, None, game_state):
        return

    for monitorId in range(1,5):
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.ENGINE_BROKEN})

def AC_ADD_4_BATTARIES_TASKS(master, task, game_state):
    # Add req all batteries
    game_state.add_active_task_with_id(101)
    # One by one 
    game_state.add_active_task_with_id(151)
    game_state.add_active_task_with_id(152)
    game_state.add_active_task_with_id(153)
    game_state.add_active_task_with_id(154)


def REQ_CHECK_BATTARIES(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery_1 = buttons[CB_CTRL.BATTERY_1]
    battery_2 = buttons[CB_CTRL.BATTERY_2]
    battery_3 = buttons[CB_CTRL.BATTERY_3]
    battery_4 = buttons[CB_CTRL.BATTERY_4]
    # print("REQ_CHECK_BATTARIES")
    batteryState = (battery_1 and battery_2 and battery_3 and battery_4)

    if not batteryState:
        return batteryState

    taskList = [151, 152, 153, 154]
    for taskId in taskList:
        task = game_state.find_task_with_id(taskId)
        game_state.remove_active_task(task)
    return True

def sendBatteryMessage(game_state, monitorId, battery, batteryId):
    if battery:
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.BATTERY_AVALIABLE.format(id=batteryId)})
    else:
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.BATTERY_ABSENT.format(id=batteryId)})

def REQ_CHECK_BATTERY_1(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_1]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 1

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def REQ_CHECK_BATTERY_2(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_2]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 2

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def REQ_CHECK_BATTERY_3(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_3]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 3

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def REQ_CHECK_BATTERY_4(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    battery = buttons[CB_CTRL.BATTERY_4]

    monitorId = game_state.getMonitorIdByTask(task)

    batteryId = 4

    sendBatteryMessage(game_state, monitorId, battery, batteryId)
    return False

def AC_PRESS_HERABORA(master, task, game_state):
    for monitorId in range(1,5):
        game_state.quest_room.send_ws_message(str(monitorId), {'message': MESSAGE.PRESS_HERABORA})

    game_state.add_active_task_with_id(2)

def REQ_CHECK_HERABORA(master, task, game_state):
        heraboraPressed = master.getButtons(CB_SLAVE_2).get()[12]
        #print("Herabora value: {}\n", heraboraPressed)
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

# Panel 1_2

def REQ_TETRAGEKS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.TETRAGEKS]

def REQ_TETRAGEKS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.TETRAGEKS]

def REQ_C3PO_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.C3PO]

def REQ_C3PO_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.C3PO]

def REQ_R2D2_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.R2D2]

def REQ_R2D2_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.R2D2]

def REQ_REPAIR_NANOROBOTS_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.REPAIR_NANOROBOTS]

def REQ_REPAIR_NANOROBOTS_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.REPAIR_NANOROBOTS]

def REQ_ULTRAFOTON_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 1 == buttons[CB_CTRL.ULTRAFOTON]

def REQ_ULTRAFOTON_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_1).get()
    return 0 == buttons[CB_CTRL.ULTRAFOTON]

# Panel 2_3

def REQ_TPBACH_1_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.TPBACH_1]

def REQ_TPBACH_1_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.TPBACH_1]

def REQ_TPBACH_2_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.TPBACH_2]

def REQ_TPBACH_2_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.TPBACH_2]

def REQ_ECO_LAZER_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.ECO_LAZER]

def REQ_ECO_LAZER_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.ECO_LAZER]

def REQ_DARK_MATTER_STABILIZER_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.DARK_MATTER_STABILIZER]

def REQ_DARK_MATTER_STABILIZER_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.DARK_MATTER_STABILIZER]

def REQ_DVORNIKI_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.DVORNIKI]

def REQ_DVORNIKI_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.DVORNIKI]

def REQ_PROTON_LAUNCHERS_BATTERY_ON(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.PROTON_LAUNCHERS_BATTERY]

def REQ_PROTON_LAUNCHERS_BATTERY_OFF(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 0 == buttons[CB_CTRL.PROTON_LAUNCHERS_BATTERY]

def REQ_HYPER_DRIVE_GENERATOR_TO_MAX(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 255 == adc[CB_CTRL.HYPER_DRIVE_GENERATOR]

def REQ_HYPER_DRIVE_GENERATOR_TO_MIN(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.HYPER_DRIVE_GENERATOR]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_3(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 130 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_2(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 86 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_1(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 45 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_DIPSOMANIA_SUPERCHARGER_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.DIPSOMANIA_SUPERCHARGER]

def REQ_CHAMAEMELUM_NOBILE_TO_3(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 255 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CHAMAEMELUM_NOBILE_TO_2(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 182 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CHAMAEMELUM_NOBILE_TO_1(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 86 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CHAMAEMELUM_NOBILE_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.CHAMAEMELUM_NOBILE]

def REQ_CONDENSER_TO_3(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 255 == adc[CB_CTRL.CONDENSER]

def REQ_CONDENSER_TO_2(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 183 == adc[CB_CTRL.CONDENSER]

def REQ_CONDENSER_TO_1(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 87 == adc[CB_CTRL.CONDENSER]

def REQ_CONDENSER_TO_0(master, task, game_state):
    adc = master.getAdc(CB_SLAVE_2).get()
    return 0 == adc[CB_CTRL.CONDENSER]

def REQ_HERABORA_PRESSED(master, task, game_state):
    buttons = master.getButtons(CB_SLAVE_2).get()
    return 1 == buttons[CB_CTRL.HERABORA]
