
CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"

def REC_ENGINE_ASSEMBLED(master, task, game_state):
	return True

def AC_ADD_4_BATARIES_TASK(master, task, game_state):
	game_state.add_active_task_with_id(1)


def REC_CHECK_BATTARIES(master, task, game_state):
	return True


def REC_CHECK_BATTARIES(master, task, game_state):
	return True

def AC_PRESS_HERABORA(master, task, game_state):
	add_active_task_with_id(2)

def REC_CHECK_HERABORA(master, task, game_state):
	heraboraPressed = master.getButtons(CB_SLAVE_2).get()[12]
	return heraboraPressed

def AC_CB_ADD_RANDOM_TASK(master, task, game_state):

	avaliableTaskIds = game_state.getAvaliableCBTaskIds()
	randomId = random.randInt(0, len(avaliableTaskIds) -1)
	game_state.add_active_task_with_id(avaliableTaskIds[randomId])

def AC_ADD_END_GAME_TASK(master, task, game_state):
	game_state.add_active_task_with_id(3)

def REC_AMOUNT_OF_TASK_SUCCESSED(master, task, game_state):
	return False

def AC_ENTERED_DOOR_OPEN(master, task, game_state):
	print("Entered door opened")

def AC_SHOW_SUCCESS_MESSAGE(master, task, game_state):
	print("You are WINNER!")

	
def REC_AMOUNT_OF_TASK_FAILURE(master, task, game_state):
	return False

def AC_SHOW_FAILURE_MESSAGE(master, task, game_state):
	print("You lose")


# Tasks

class Cb1Buttons:
	pass

class Cb2Buttons:
	PRESLO = 0
	KOKOVNIK = 1
	TRUNDEL = 2
	GLUKALO = 3

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





