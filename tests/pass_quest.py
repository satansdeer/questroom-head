import Pyro.naming, Pyro.core
from Pyro.errors import NamingError

import time

# locate the NS
locator = Pyro.naming.NameServerLocator()
print('Searching Name Server...'),
ns = locator.getNS()

# resolve the Pyro object
print('finding object')
try:
        URI=ns.resolve('DEVICE_MASTER')
        print('URI:',URI)
except (NamingError, x):
        print('Couldn\'t find object, nameserver says:'),
        raise SystemExit


CB_SLAVE_1="CB_SLAVE_1"
CB_SLAVE_2="CB_SLAVE_2"
hallwayPuzzles = "hallwayPuzzles"

class Buttons:

    # hallway controller
    WIRE_CONNECTION = 11
    FUSE = 6
    MECHANICS_CARD = 10
    ROBOT_HEAD = 8
    ENGINE = 9
    COMMUTATOR = 7

    # Controller 1
    #    # Buttons
    REPULSIVE_DESYNCRONISER = 0
    LEVITRON = 1
    DEFLECTOR = 2
    BIG_RED_BUTTON = 3
    KRIVOSHUP_MINUS = 4
    KRIVOSHUP_PLUS = 5
    SERVO_COOLING_SYSTEM = 6
    ULTRAFOTON = 13
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
    TECHNO = 13
    UGNETATEL = 14
    GIPERBOLOID = 15
    ZOND_JS = 16
    ZOND_JC = 17

    #    # ADC
    CHAMAEMELUM_NOBILE = 0
    DIPSOMANIA_SUPERCHARGER = 1
    HYPER_DRIVE_GENERATOR = 2
    CONDENSER = 7

    DOOR_ENTER = 1
    DOOR_ENGINE = 2
    DOOR_CAPTAIN = 3
class Adc:
    RADIO = 0
    BOX_LOCK = 1

def pass_wire():
    print("PASS WIRE")
    buttons = master.getButtons(hallwayPuzzles, "value")
    buttons[Buttons.WIRE_CONNECTION] = 1
    master.setButtons(hallwayPuzzles, buttons)

def pass_fuse():
    print("PASS FUSE")
    buttons = master.getButtons(hallwayPuzzles, "value")
    buttons[Buttons.FUSE] = 1
    master.setButtons(hallwayPuzzles, buttons)

def switching_radio():
    print("SWITCHING RADIO")
    step = 50
    delay_time = 2

    adcs = master.getAdc(hallwayPuzzles, "value")
    for radio_value in range(0, 255, step):
        adcs[Adc.RADIO] = radio_value
        master.setAdc(hallwayPuzzles, adcs)
        time.sleep(delay_time)


    adcs[Adc.RADIO] = 0
    master.setAdc(hallwayPuzzles, adcs)

def open_first_box_lock():
    print("OPEN FIRST BOX")
    delay_time = 5
    code_sequence = [56, 73, 90, 73, 90]

    adcs = master.getAdc(hallwayPuzzles, "value")
    for code_value in code_sequence:
        adcs = master.getAdc(hallwayPuzzles, "value")
        print("Adc: {}".format(adcs))
        adcs[Adc.BOX_LOCK] = code_value
        master.setAdc(hallwayPuzzles, adcs)
        time.sleep(delay_time)

def use_mechanics_card():
    print("Use mechanic card")
    buttons = master.getButtons(hallwayPuzzles, "value")
    buttons[Buttons.MECHANICS_CARD] = 1
    master.setButtons(hallwayPuzzles, buttons)

def pass_tumbler_puzzle():

    ELEMENTS_NUMBER = 6
    VISIBLE_SWITCHERS_START_NUM = 12
    VISIBLE_SWITCHERS_END_NUM = 17

    def turn_switcher(position):
        print("Turn swither: {}".format(position))
        buttons = master.getButtons(hallwayPuzzles, "value")
        # get values from visible Panel
        visiblePanelSwitchers = buttons[VISIBLE_SWITCHERS_START_NUM:
                VISIBLE_SWITCHERS_END_NUM + 1]
        # doing reverse because num 12 in buttons is 6 on panel
        visiblePanelSwitchers.reverse()

        switchers = visiblePanelSwitchers

        switchers[position] = ~switchers[position] & 0x1
        switchers.reverse()

        buttons[VISIBLE_SWITCHERS_START_NUM:
                VISIBLE_SWITCHERS_END_NUM + 1] = switchers

        master.setButtons(hallwayPuzzles, buttons)
        print("Buttons: {}".format(buttons))
        time.sleep(0.5)

    turn_switcher(0)
    turn_switcher(0)

    turn_switcher(1)
    turn_switcher(1)

    turn_switcher(2)
    turn_switcher(2)

    turn_switcher(3)
    turn_switcher(3)
    turn_switcher(3)
    turn_switcher(3)

    turn_switcher(4)
    turn_switcher(4)
    turn_switcher(4)
    turn_switcher(4)

    turn_switcher(5)
    turn_switcher(5)
    turn_switcher(5)
    turn_switcher(5)

def assembled_robot():
    buttons = master.getButtons(hallwayPuzzles, "value")
    buttons[Buttons.ROBOT_HEAD] = 1
    master.setButtons(hallwayPuzzles, buttons)

def pass_commutator():
    buttons = master.getButtons(hallwayPuzzles, "value")
    buttons[Buttons.COMMUTATOR] = 1
    master.setButtons(hallwayPuzzles, buttons)

def assembled_engine():
    buttons = master.getButtons(hallwayPuzzles, "value")
    buttons[Buttons.ENGINE] = 1
    master.setButtons(hallwayPuzzles, buttons)

def insert_batteries():
    print("INSERT BATTERIES")

    buttons = master.getButtons(CB_SLAVE_2, "value")

    print("insert 1 batterie")
    buttons[Buttons.BATTERY_1] = 1
    master.setButtons(CB_SLAVE_2, buttons)

    time.sleep(2)
    print("insert 2 batterie")
    buttons[Buttons.BATTERY_2] = 1
    master.setButtons(CB_SLAVE_2, buttons)

    time.sleep(2)
    print("insert 3 batterie")
    buttons[Buttons.BATTERY_3] = 1
    master.setButtons(CB_SLAVE_2, buttons)

    time.sleep(2)
    print("insert 4 batterie")
    buttons[Buttons.BATTERY_4] = 1
    master.setButtons(CB_SLAVE_2, buttons)

def press_herabora():
    buttons = master.getButtons(CB_SLAVE_2, "value")
    buttons[Buttons.HERABORA] = 1
    master.setButtons(CB_SLAVE_2, buttons)

    time.sleep(2)
    buttons[Buttons.HERABORA] = 0
    master.setButtons(CB_SLAVE_2, buttons)

def play_game():
    def inverse_buttons(buttons):
        for index, button in enumerate(buttons):
            buttons[index] = (~button) & 0x1

    def pass_stage():
        buttons_controller_1 = master.getButtons(CB_SLAVE_1, "value")
        inverse_buttons(buttons_controller_1)
        master.setButtons(CB_SLAVE_1, buttons_controller_1)
        time.sleep(2)


        buttons_controller_2 = master.getButtons(CB_SLAVE_2, "value")
        inverse_buttons(buttons_controller_2)
        master.setButtons(CB_SLAVE_2, buttons_controller_2)

    time.sleep(3)
    pass_stage()
    time.sleep(2)
    pass_stage()

# create a proxy for the Pyro object, and return that
remote_master = Pyro.core.getProxyForURI(URI)
master = remote_master

pass_wire()
time.sleep(3) # delays for wait colors effects

pass_fuse()
time.sleep(5)

switching_radio()
time.sleep(1)

open_first_box_lock()

use_mechanics_card()
time.sleep(1)

pass_tumbler_puzzle()

assembled_robot()
time.sleep(1)

pass_commutator()
time.sleep(1)

raw_input("Please enter something: ")

assembled_engine()
time.sleep(1)

insert_batteries()
time.sleep(1)
raw_input("Please enter something: ")

press_herabora()
time.sleep(35)

press_herabora()

time.sleep(2)
while True:
    play_game()

