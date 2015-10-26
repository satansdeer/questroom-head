#!/usr/bin/python
# -*- coding: utf-8 -*-

# import random
import serial
# import time

# Класс формирования пакета
from spacePackage import *
logDevice = logging.getLogger('device')


class SpaceDevice:
    # константы размера списка элементов платы
    NUM_SIMPLE_LEDS = 80
    NUM_SMART_LEDS = 96
    NUM_SMART_LEDS_BYTE = NUM_SMART_LEDS * 3
    NUM_SIMPLE_BUTTONS = 18
    NUM_RELAYS = 4
    NUM_ADC = 8
    NUM_SENSOR = 2
    NUM_ENCODERS = 4

    # константы ожидаемого кол-ва байт в ответе от слейва
    class AnswerBytes:
        # Сумма стартового байта, команды и CRC
        startCommandCRCBytes = 5
        # кол-во байт пакета на один байт данных
        numPackageBytes = 2
        # байтов в ответе по умолчанию
        default = 100

        connectionCheck = startCommandCRCBytes + numPackageBytes * 7
        setSimpleLEDs = startCommandCRCBytes
        setSmartLEDs = startCommandCRCBytes
        setLCD = startCommandCRCBytes
        setRelays = startCommandCRCBytes
        getButtons = startCommandCRCBytes + numPackageBytes * 3
        getFreezeButtons = startCommandCRCBytes + numPackageBytes * 3
        getADC = startCommandCRCBytes + numPackageBytes * 8
        getEncoders = startCommandCRCBytes + numPackageBytes * 8
        getSensors = startCommandCRCBytes + numPackageBytes * 2
        unknown = startCommandCRCBytes + numPackageBytes * 1
        dictAB = {
            Command.connectionCheck: connectionCheck,
            Command.setSimpleLEDs: setSimpleLEDs,
            Command.setSmartLEDs: setSmartLEDs,
            Command.setLCD: setLCD,
            Command.setRelays: setRelays,
            Command.getButtons: getButtons,
            Command.getStuckButtons: getFreezeButtons,
            Command.getADC: getADC,
            Command.getEncoder: getEncoders,
            Command.getSensor: getSensors,
            Command.unknown: unknown
        }

    __simpleLEDsArray = [0] * NUM_SIMPLE_LEDS
    __smartLEDsArray = [0] * NUM_SMART_LEDS
    __relayArray = [0] * NUM_RELAYS

    __simpleButtonsArray = [0]*NUM_SIMPLE_BUTTONS
    __ADCArray = [0] * NUM_ADC
    __encoderArray = [0] * NUM_ENCODERS
    __sensorArray = [0] * NUM_SENSOR

    __address = 0
    __portDescriptor = None
    __name = None

    __connection = False

    def __init__(self, address, portDescriptor, name=None):
        self.__address = address
        self.__portDescriptor = portDescriptor
        self.__name = name

    def sendConnectionCheck(self):
        logDevice.debug("ConnectionCheck")
        message = self._sendCommand(Command.connectionCheck)
        if message:
            helloStr = ''
            for char in message:
                helloStr += chr(char)
            logDevice.debug("We receive by connectionCheck "
                            "command: %s", helloStr)
            self.__connection = True
            return True
        self.__connection = False
        return False

    # Set Commands
    def sendSetSimpleLEDs(self, diodes):
        logDevice.debug("Set SimpleLEDs")
        status = self._sendCommand(Command.setSimpleLEDs, diodes)
        success = self._checkSetCommandStatus(status)
        if success:
            self._saveSimpleLEDs(diodes)
            return True
        return False

    def sendSetSmartLEDs(self, diodes):
        logDevice.debug("Set SmartLEDs")
        status = self._sendCommand(Command.setSmartLEDs, diodes)
        success = self._checkSetCommandStatus(status)
        if success:
            self._saveSmartLEDs(diodes)
            return True
        return False

    def sendSetLCD(self, message):
        logDevice.debug("set LCD")
        status = self._sendCommand(Command.setLCD, message)
        return self._checkSetCommandStatus(status)

    def sendSetRelays(self, relays):
        # 4 реле; на входе список из 4 значений 0 1
        logDevice.debug("set Relay")
        status = self._sendCommand(Command.setRelays, relays)
        success = self._checkSetCommandStatus(status)
        if success:
            self._saveRelays(relays)
            return True
        return False

    # Get Commands
    def sendGetButtons(self):
        logDevice.debug("get Buttons Value")
        buttonsList = self._sendCommand(Command.getButtons)
        if buttonsList:
            self._saveButtons(buttonsList)
            return True
        return False

    def sendGetStuckButtons(self):
        logDevice.debug("get Buttons Value")
        buttonsList = self._sendCommand(Command.getStuckButtons)
        if buttonsList:
            self._saveButtons(buttonsList)
            return True
        return False

    def sendGetADC(self):
        logDevice.debug("get ADC")
        adcList = self._sendCommand(Command.getADC)
        if adcList:
            self._saveADC(adcList)
            return True
        return False

    def sendGetEncoder(self):
        logDevice.debug("get Encoder")
        encodersList = self._sendCommand(Command.getEncoder)
        if encodersList:
            self._saveEncoders(encodersList)
            return True
        return False

    def sendGetSensorButtons(self):
        logDevice.debug("get Sensor Buttons")
        sensorValue = self._sendCommand(Command.getSensor)
        if sensorValue:
            self._saveSensors(sensorValue)
            return True
        return False

    def sendUncknownCommand(self):
        logDevice.debug("Uncknown Commad with code: %d", Command.unknown)
        result = self._sendCommand(Command.unknown)
        if result:
            return True
        return False

    def _getNumAnswerBytes(self, command):
        numBytes = self.AnswerBytes.dictAB.get(command)
        if (numBytes is None):
            return self.AnswerBytes.default
        else:
            return numBytes

    def sendCommand(self, command, data):
        sendOk = False
        # Set Command
        if (Command.connectionCheck == command):
            sendOk = self.sendConnectionCheck()
        elif(Command.setSimpleLEDs == command):
            sendOk = self.sendSetSimpleLEDs(data)
        elif(Command.setSmartLEDs == command):
            sendOk = self.sendSetSmartLEDs(data)
        elif(Command.setLCD == command):
            sendOk = self.sendSetLCD(data)
        elif(Command.setRelays == command):
            sendOk = self.sendSetRelays(data)
        # Get Command
        elif(Command.getButtons == command):
            sendOk = self.sendGetButtons()
        elif(Command.getStuckButtons == command):
            sendOk = self.sendGetStuckButtons()
        elif(Command.getADC == command):
            sendOk = self.sendGetADC()
        elif(Command.getEncoder == command):
            sendOk = self.sendGetEncoder()
        elif(Command.getSensor == command):
            sendOk = self.sendGetSensorButtons()
        # Special Unknown command
        elif(Command.unknown == command):
            sendOk = self.sendUncknownCommand()
        # answerBytes = self._getNumAnswerBytes(command)
        # self._sendCommand(command, data, answerBytes)
        return sendOk

    def _sendCommand(self, command, data=None):
        # Формирование пакета для отправки
        package = SpacePackage()
        packageToSend = package.createPackage(
            self.getAddress(),
            command, data)

        self._printBytes(packageToSend, "Send")

        # Оправка пакета
        bytesSend = self.__portDescriptor.write(packageToSend)
        logDevice.debug("We send: %d bytes", bytesSend)

        # Получение ответа
        bytesReceive = None
        answerBytes = self._getNumAnswerBytes(command)
        bytesReceive = self.__portDescriptor.read(answerBytes)

        if bytesReceive:
            logDevice.debug("We receive something")
            self._printBytes(bytesReceive, "Receive")
        else:
            logDevice.debug("Timeout: We receive Nothing")

        answer = package.parseAnswerPackage(
            self.getAddress(), command, bytesReceive)
        if answer is not None:
            self._printBytes(answer, "Answer")
            return answer

        return None

    def getAddress(self):
        return self.__address

    def getName(self):
        return self.__name

    # Simple LED's
    def getSimpleLEDs(self):
        return self.__simpleLEDsArray

    def _saveSimpleLEDs(self, LEDs):
        if len(LEDs) < self.NUM_SIMPLE_LEDS:
            self.__simpleLEDsArray = LEDs + [0] * \
                (self.NUM_SIMPLE_LEDS - len(LEDs))
        else:
            self.__simpleLEDsArray = LEDs[0: self.NUM_SIMPLE_LEDS]

    # Smart LED's
    def getSmartLEDs(self):
        return self.__smartLEDsArray

    def _saveSmartLEDs(self, LEDs):
        if len(LEDs) < self.NUM_SIMPLE_LEDS:
            self.__smartLEDsArray = LEDs + [0] * (self.NUM_SMART_LEDS - len(LEDs))
        else:
            self.__smartLEDsArray = LEDs[0: self.NUM_SMART_LEDS]

    # Simple Buttons
    def getButtons(self):
        return self.__simpleButtonsArray

    def _saveButtons(self, buttons):
        if len(buttons) < self.NUM_SIMPLE_BUTTONS:
            self.__simpleButtonsArray = buttons + [0] * \
                                        self.NUM_SIMPLE_BUTTONS - len(buttons)
        else:
            self.__simpleButtonsArray = buttons[0: self.NUM_SIMPLE_BUTTONS]

    # Relays
    def getRelays(self):
        return self.__relayArray

    def _saveRelays(self, relays):
        if len(relays) < self.NUM_RELAYS:
            self.__relayArray = relays + [0] * (self.NUM_RELAYS - len(relays))
        else:
            self.__relayArray = relays[0: self.NUM_RELAYS]

    # ADC
    def getADC(self):
        return self.__ADCArray

    def _saveADC(self, adcList):
        if len(adcList) < self.NUM_ADC:
            self.__ADCArray = adcList + [0] * (self.NUM_ADC - len(adcList))
        else:
            self.__ADCArray = adcList[0:self.NUM_ADC]

    # Encoders
    def getEncoders(self):
        return self.__encoderArray

    def _saveEncoders(self, encodersList):
        if len(encodersList) < self.NUM_ENCODERS:
            self.__encoderArray = encodersList + [0] * \
                (self.NUM_ENCODERS - len(encodersList))
        else:
            self.__encoderArray = encodersList[0: self.NUM_ENCODERS]

    def getSensors(self):
        return self.__sensorArray

    def _saveSensors(self, sensorList):
        if len(sensorList) < self.NUM_SENSOR:
            self.__sensorArray = self.NUM_SENSOR + [0] * \
                (self.NUM_SENSOR - len(sensorList))
        else:
            self.__sensorArray = sensorList[0: self.NUM_SENSOR]

    def connection(self):
        return self.__connection

    def _printBytes(self, _bytes, receiveSend=''):
        index = 0
        for byteR in _bytes:
            index += 1
            # Отправляем мы массив байт, а получаем массив str
            # так что надо проверить, и если необходимо преобразовать в int
            if isinstance(byteR, int):
                binHexStr = "int: {0:>5d} hex: 0x{0:>02x}   bin: 0b{0:>08b}".format(byteR)
            else:
                binHexStr = "int: {0:>5d} hex: 0x{0:>02x}   bin: 0b{0:>08b}".format(ord(byteR))

            logDevice.debug(" %s [%2d] %s",
                            receiveSend,
                            index,
                            binHexStr)

    def _checkSetCommandStatus(self, status):
        if status:
            if status[0] == 0x80:
                logDevice.debug("Slave receive and "
                                "understand our command: 0x80")
                return True
            logDevice.info("Command send failure")
        return False


class SmartLEDs:
    Red = 0
    Green = 0
    Blue = 0

if __name__ == '__main__':
    # logging.debug('This is a debug message')

    # Либо COM1 COM2 COM3 для Windows
    # Либо com-порт в /dev/ для Linux
    ser = serial.Serial('ptyp1', 9600, timeout=1, writeTimeout=2,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)

    device = SpaceDevice(1, ser)

    # Проверка связи: результат в консоли. поскольку никуда не сохраняется
    # device.sendConnectionCheck()

    # Тестируем обычные светодиоды
    # data = [int(2*random.random()) for i in xrange(80)]
    data = [1, 0] * 40
    data[2] = 1
    data[33] = 1
    # device.sendSetSimpleLEDs(data)

    # Тестируем умные светодиоды
    smartLEDsList = [0x0A, 0x0A, 0x0A] * 96
    smartLEDsList[287] = 3
    smartLEDsList[286] = 2
    smartLEDsList[285] = 1
    # device.sendSetSmartLEDs(smartLEDsList)

    # ЖКИ
    message = "Hello"
    # device.sendSetLCD(message)

    # Реле
    releys = [1, 0, 0, 0]
    # device.sendSetRelays(releys)

    # Получить значения кнопок
    # device.sendGetButtons()
    # buttons = device.getButtons()
    # print "Buttons value: ", buttons

    # АЦП. Получить значения слайдеров и крутилок
    # device.sendGetADC()
    # adcList = device.getADC()
    # print "ADC value: ", adcList

    # # Получить значения энкодеров
    device.sendGetEncoder()
    encodersList = device.getEncoders()
    print "Encoders value: ", encodersList

    # # Получить значения сенсорных кнопок
    # device.sendGetSensorButtons()
    # sensorList = device.getSensors()
    # print "Sensor values: ", sensorList

    # print data
    # while True:
    #     # time.sleep(1)
    #
    #     time.sleep(0.5)
    #
