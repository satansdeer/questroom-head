#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import serial
import time
import logging

# для отладочного вывода
logging.basicConfig(
    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s%(message)s',
    level=logging.DEBUG)
logPackage = logging.getLogger('package')
logging.disable(logging.DEBUG)



CODE_KEY = 'code'
LENGTH_DATA_KEY = 'lengthData'


class Command:
    connectionCheck = 0x00
    setSimpleLEDs = 0x10
    setSmartLEDs = 0x11
    setLCD = 0x12
    setRelays = 0x13

    getButtons = 0x20
    getADC = 0x21
    getEncoder = 0x22
    getSensor = 0x23
    getStuckButtons = 0x24
    unknown = 0x56

class SpacePackage:

    class PackageIndicator:
        new, old = range(2)

    class TetradeType:
        shift = 6  # сдвиг влево
        hight = 0x01 << shift
        low = 0x00 << shift

    class ByteType:
        shift = 4
        command = 0x00 << shift
        data = 0x01 << shift
        crc = 0x02 << shift
        reserved = 0x03 << shift

    def createPackage(self, address, command, data):
        package = None
        # Set Command
        if (Command.connectionCheck == command):
            package = self._createConnectionCheckPackage(address, command,
                                                         data)
        elif(Command.setSimpleLEDs == command):
            package = self._createSetSimpleLEDsPackage(address, command, data)

        elif(Command.setSmartLEDs == command):
            package = self._createSetSmartLEDsPackage(address, command, data)

        elif(Command.setLCD == command):
            package = self._createSetLCDPackage(address, command, data)

        elif(Command.setRelays == command):
            package = self._createSetRelaysPackage(address, command, data)

        # Get Command
        elif(Command.getButtons == command):
            package = self._createGetButtons(address, command, data)
        elif(Command.getStuckButtons == command):
            package = self._createGetStuckButtons(address, command, data)
        elif(Command.getADC == command):
            package = self._createGetADCPackage(address, command, data)

        elif(Command.getEncoder == command):
            package = self._createGetEncoderPackage(address, command, data)

        elif(Command.getSensor == command):
            package = self._createGetSensorPackage(address, command, data)

        # Special Unknown command
        elif(Command.unknown == command):
            package = self._createUnknownCommandPackage(address, command, data)

        return package

    def _countPackageCRC(self, package):
        # контрольная сумма - младший байт суммы всех байтов пакета кроме
        # # самой контрольной суммы
        crc = 0
        for packageByte in package:
            # Отправляем мы массив байт, а получаем массив str
            # так что надо проверить, и если необходимо преобразовать в int
            if isinstance(packageByte, int):
                intByte = packageByte
            else:
                intByte = ord(packageByte)
            crc += intByte
        crcL = crc & 0xff
        logPackage.debug("CRC: %s Lbyte: %s",
                         "{0}(0b{0:08b})".format(crc), bin(crcL))
        return crcL

    def _createPackageByte(self, packageIndicator, byteType,
                           tetradeType, address, data):
        # создаём стартовый байт
        if (self.PackageIndicator.new == packageIndicator):
            # установиливаем 7 бит: признак начала новой посылки
            packageByteStart = 0b10000000
            # добавляем адрес в поле данных
            packageByteStart |= address
            # print 'Start package byte: ', bin(packageByteStart)
            return packageByteStart
        # создание байтов остальных типов
        # - обнулим старшую тетраду на всякий случай
        data &= 0b00001111
        packageByte = 0x00
        packageByte |= byteType | tetradeType | data
        return packageByte

    # Функция создания байтов команды для пакета
    def _createCommandBytes(self, command):
        # создание байтов команды
        # получаем старшую тетраду кода команды
        commandCodeH = command >> 4
        # - старший байт
        commandByteH = self._createPackageByte(
            None, self.ByteType.command,
            self.TetradeType.hight, None,
            commandCodeH)

        # - младший байт
        commandCodeL = command & 0x0f
        commandByteL = self._createPackageByte(
            None, self.ByteType.command,
            self.TetradeType.low, None,
            commandCodeL)
        return [commandByteH, commandByteL]

    # Функция преобразующая байт данных в два пакетных байта
    def _createPackageDataBytes(self, dataByte):
        # разделяем на старшую и младшую тетрады
        dataValueH = dataByte >> 4
        dataValueL = dataByte & 0x0f

        dataByteH = self._createPackageByte(None, self.ByteType.data,
                                            self.TetradeType.hight,
                                            None, dataValueH)
        dataByteL = self._createPackageByte(None, self.ByteType.data,
                                            self.TetradeType.low,
                                            None, dataValueL)
        return [dataByteH, dataByteL]

    # Функция формирования байтов контрольной суммы для пакета
    def _createCRCPackageBytes(self, package):
        crcByte = self._countPackageCRC(package)
        crcValueH = crcByte >> 4
        crcValueL = crcByte & 0x0f
        crcByteH = self._createPackageByte(None, self.ByteType.crc,
                                           self.TetradeType.hight,
                                           None, crcValueH)
        crcByteL = self._createPackageByte(None, self.ByteType.crc,
                                           self.TetradeType.low,
                                           None, crcValueL)
        return [crcByteH, crcByteL]

    # 1 Создание пакета для команды проверки связи
    def _createConnectionCheckPackage(self, address, command, data):
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commadBytes = self._createCommandBytes(Command.connectionCheck)
        package.extend(commadBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 2 Создание пакета для установки значения простых светодиодов
    def _createSetSimpleLEDsPackage(self, address, command, data):
        # создание байта начала посылки
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commadBytes = self._createCommandBytes(Command.setSimpleLEDs)
        package.extend(commadBytes)

        # упаковываем данные
        for dataBayteId in range(0, len(data), 8):
            dataByteList = data[dataBayteId:dataBayteId+8]

            # преобразуем массив битов в Байт
            # в старшем бите байта светодиод со старшим номером
            # print 'DataByteList: ', dataByteList
            dataByte = 0x00
            for dataBit in reversed(dataByteList):
                dataByte = dataByte << 1
                dataByte |= dataBit

            dataPackageBytes = self._createPackageDataBytes(dataByte)
            package.extend(dataPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 3 - Создание пакета для установки значений умных светодиодов
    # 24 * 4 = 96 LEDs; 96 * 3  = 288 - элментов в списке data
    def _createSetSmartLEDsPackage(self, address, command, data):
        # создание байта начала посылки
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commadBytes = self._createCommandBytes(Command.setSmartLEDs)
        package.extend(commadBytes)

        # упаковываем данные
        # Каждый светодиод описывается 3мя тетрадами (12 битами).
        # Т.е. 12 бит – самого старшего светодиода, потом 12 бит
        # предыдущего и т.д.
        # Видно, что некоторые байты перехлестываются:
        # старшая часть байта отвечает за один светодиод,
        # младшая – за другой. В одной микросхеме 24 канала (24 светодиода).
        # Таких микросхем 4е.
        # Итого 4 микросхемы * 24 канала * 12 бит / 8 бит = 144 байта.
        # 144 байта * 2 = 288 байт данных в пакете + 2 crc + 3 st com
        # = 293 байта в пакете
        # меняем порядок тетрад
        # H M L -> L M H
        reversed12BitData = []
        for brightness12Bit in data:
            # выделяем из 12 битового числа тетрады
            brightH = (brightness12Bit & 0xf00) >> 8
            brightM = (brightness12Bit & 0x0f0) >> 4
            brightL = (brightness12Bit & 0x00f)
            # сохраняем тетрады в обратном порядке, чтобы правильно перевернуть
            reversedBrightness = [brightL, brightM, brightH]
            reversed12BitData.extend(reversedBrightness)

        # делаем старший светодиод(последний) первым
        reversed12BitData = list(reversed(reversed12BitData))

        # Последовательно запихиваем тетрады в байт пакета
        dataByte = 0x00
        for tetradeH, tetradeL in zip(reversed12BitData[0::2],
                                      reversed12BitData[1::2]):
            tetradeH &= 0x0f
            tetradeL &= 0x0f
            dataByte = tetradeH << 4
            dataByte |= tetradeL
            dataPackageBytes = self._createPackageDataBytes(dataByte)
            package.extend(dataPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 4 Создание пакета отображения сообщения на ЖКИ
    # Нам приходит строка на 80 символов. Или меньше. То остальное пустое
    def _createSetLCDPackage(self, address, command, data):
        # создание байта начала посылки
        LCD_STRING_lENGTH = 80
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commadBytes = self._createCommandBytes(Command.setLCD)
        package.extend(commadBytes)

        # добавляем пустое место, если входящая строка меньше
        if len(data) < LCD_STRING_lENGTH:
            dataStr = data + (' ' * (LCD_STRING_lENGTH - len(data)))
        elif len(data) == LCD_STRING_lENGTH:
            dataStr = data
        else:
            dataStr = data[0:LCD_STRING_lENGTH]

        for charStr in dataStr:
            dataPackageBytes = self._createPackageDataBytes(ord(charStr))
            package.extend(dataPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 5 Создание пакета установки значений реле
    def _createSetRelaysPackage(self, address, command, data):
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commadBytes = self._createCommandBytes(Command.setRelays)
        package.extend(commadBytes)

        # упаковываем данные
        for dataBayteId in range(0, len(data), 8):  # = [0]
            dataByteList = data[dataBayteId:dataBayteId + 8]
            # преобразуем массив битов в Байт
            # бит 4 - реле 1; бит 5 - реле 2
            # Биты байта в данных: от старшего к младшему

            # поэтому разворачиваем значения в обратном порядке
            # запихиваем в байт побитно, каждый раз сдвигая влево
            dataByte = 0x00
            reversedData = reversed(dataByteList)
            for dataBit in reversedData:
                dataByte = dataByte << 1
                dataByte |= dataBit
            dataByte = dataByte << 4

            dataPackageBytes = self._createPackageDataBytes(dataByte)
            package.extend(dataPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 6 Создание пакета запроса на получение значений кнопок
    def _createGetButtons(self, address, command, data):
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        # создание байтов команды
        commandPackageBytes = self._createCommandBytes(Command.getButtons)
        package.extend(commandPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 6.2 Создание пакета запроса на получение значений залипших кнопок
    def _createGetStuckButtons(self, address, command, data):
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        # создание байтов команды
        commandPackageBytes = self._createCommandBytes(Command.getStuckButtons)
        package.extend(commandPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 7 - Создание пакета запроса на получние значений слайдеров и резистивных
    #       крутилок (каналы АЦП)
    def _createGetADCPackage(self, address, command, data):
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commandPackageBytes = self._createCommandBytes(Command.getADC)
        package.extend(commandPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 8 - Создание пакета запроса на получение значений энкодеров
    def _createGetEncoderPackage(self, address, command, data):
        package = []

        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        # создаём байты команды
        commandPackageBytes = self._createCommandBytes(Command.getEncoder)
        package.extend(commandPackageBytes)

        # считаем и упаковываем crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    # 9 - Создание пакета запроса на получение значений сенсорных кнопок.
    def _createGetSensorPackage(self, address, command, data):
        package = []

        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        # создаём байты команды
        commandPackageBytes = self._createCommandBytes(Command.getSensor)
        package.extend(commandPackageBytes)

        # считаем и упаковываем crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package


    # N - Создание пакета запроса c заведомо неверной командой.
    def _createUnknownCommandPackage(self, address, command, data):
        package = []

        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        # создаём байты команды
        commandPackageBytes = self._createCommandBytes(Command.unknown)
        package.extend(commandPackageBytes)

        # считаем и упаковываем crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

# Not end yet
    # find And Get index of Start Byte
    def _findStartByte(self, package, startValue):
        index = 0
        for packageByte in package:
            if ord(packageByte) == startValue:
                return index
            else:
                index += 1
        return None

    # Функция получения байта данных из двух пакетных байтов
    def _getDataFromBytes(self, hightByte, lowByte):
        hightData = (ord(hightByte) & 0x0f) << 4

        if None == lowByte:
            lowData = 0x00
        else:
            lowData = (ord(lowByte) & 0x0f)

        return hightData | lowData

    # Получение чистых данных пакета. на выходе список
    def _paresePackageData(self, package):

        # исключаем стартовый байт, байты комманды, crc
        packageData = package[3:-2]

        realData = []
        for i in range(0, len(packageData), 2):
            if len(packageData) - 1 != i:
                realDataByte = self._getDataFromBytes(
                    packageData[i], packageData[i+1])
            else:
                realDataByte = self._getDataFromBytes(
                    packageData[i], None)
            realData.extend([realDataByte])

        return realData

    # Определение валидности полученного пакета:
    #   проверка на соответствие контрольных сумм
    # байта начала посылки
    # дублирования команды
    def _receivePackageValid(self, address, command, package):
        if package:
            startByte = ord(package[0])
            logging.debug("Type for package[1]: %s value: 0x%02x",
                          type(startByte),
                          startByte)

        # считаем сrc и сравниваем с тем, что получили
        receiveCrc = self._getDataFromBytes(
                package[-2], package[-1])
        countCrcValue = self._countPackageCRC(package[:-2])

        if (receiveCrc != countCrcValue):
            logPackage.debug("Crc not equal! our count: %s | receive: %s",
                             "0x{0:02x} {0}(0b{0:08b})".format(countCrcValue),
                             "0x{0:02x} {0}(0b{0:08b})".format(receiveCrc))

            return False
        # определяем, что этот пакет нам
        if (ord(package[0]) != 0x80):
            logPackage.debug("Receive package start with: %s | Not for us",
                             "0x{0:02x} {0}(0b{0:08b})".format(
                                ord(package[0])))
            return False

        # определяем команду
        receiveCommand = self._getDataFromBytes(package[1], package[2])
        if (receiveCommand != command):
            logPackage.debug("Receive package command code: %s | Not for us",
                             "0x{0:02x} {0}(0b{0:08b})".format(receiveCommand))
            return False

        return True

    # Парсер ответа от слейва. Если пакет валидный вернёт данные
    def parseAnswerPackage(self, address, command, package):
        if package:
            packageValid = self._receivePackageValid(address, command, package)
            if not packageValid:
                return None
            # определяем данные
            receiveData = self._parseDataByCommand(command, package)

            return receiveData
        return None

    # Функция case по выбору функции для получения данных
    # в зависимости от команды
    def _parseDataByCommand(self, command, package):

        data = self._paresePackageData(package)
        # commandUnknown = self._unknownCommandData(data)
        # if (commandUnknown):
        #     return None
        if (Command.getButtons == command):
            dataForReturn = self._parseGetButtonsData(data)
        elif (Command.getStuckButtons == command):
            dataForReturn = self._parseGetButtonsData(data)
        elif(Command.getADC == command):
            dataForReturn = self._parseGetADCData(data)
        elif(Command.getEncoder == command):
            dataForReturn = self._parseGetEncoderData(data)
        elif(Command.getSensor == command):
            dataForReturn = self._parseGetSensorData(data)
        elif(Command.connectionCheck == command):
            dataForReturn = data
        else:
            # Для команд установки значений - ответ одинаковый
            dataForReturn = self._parseSetTypeCommandData(data)

        return dataForReturn

    # Проверка телеграммы от слейва. Известна ли ему команда
    def _unknownCommandData(self, data):
        if (len(data) == 1):
            if data[0] == 0x81:
                logPackage.debug("Unknown command for slave!")
                return True
        return False

    # Парсер данных пакета для команды получения значений кнопок
    # В ответ 3 байта, используемые биты 0 - 17
    def _parseGetButtonsData(self, data):
        if len(data) != 3:
            logPackage.debug("For command getButtons data length\
             must be 3 bytes but we have: %d", len(data))
            return None
        buttonsList = []
        for dataByte in data:
            for i in range(0, 8):
                button = (dataByte >> i) & 0x01
                buttonsList.append(button)
        return buttonsList

    # Парсер АЦП данных
    # В ответ 8 байт. 0 байт соответствует 0 каналу АЦП и т.д.
    def _parseGetADCData(self, data):
        if len(data) != 8:
            logPackage.debug("For command getADC data length\
             must be 8 bytes but we have: %d", len(data))
            return None
        return data

    # Парсер данных энкодера
    # В ответ 8 байт (по 2а байта на крутилку).
    # Значения LE. 0 счетчик (16 бит) соответствует 0 крутилке.
    def _parseGetEncoderData(self, data):
        if len(data) != 8:
            logPackage.debug("For command getEncoder data length\
             must be 8 bytes but we have: %d", len(data))
            return None
        encoderList = []
        for index in range(0, 8, 2):
            # значения Little-endian!
            encoderValue = (data[index + 1] << 8) | (data[index])
            encoderList.append(encoderValue)
        return encoderList

    # Парсер значений сенсорных кнопок
    # Значения от 0 до 255 для каждой кнопки, их вроде 2,
    #  так что считаем что два байта, но не будем пока ограничивать
    def _parseGetSensorData(self, data):
        return data

    # Парсер данных для команд установления значений
    def _parseSetTypeCommandData(self, data):
        if (len(data) == 1):
            if data[0] == 0x80:
                logPackage.debug("Slave Receive our Command Successful!")
                return data
        logPackage.debug("Unknown value for command in data \
            | data len = %d", len(data))
        return None

        # Функция для тестирования. Создание пакета ответа
    def createAnswerPackage(self, address, command, data):
        # создание байта начала посылки
        package = []
        startByte = self._createPackageByte(self.PackageIndicator.new,
                                            None, None, address, None)
        package.append(startByte)

        commadBytes = self._createCommandBytes(command)
        package.extend(commadBytes)

        # упаковываем данные
        for dataByte in data:
            if isinstance(dataByte, int):
                intByte = dataByte
            else:
                intByte = ord(dataByte)
            dataPackageBytes = self._createPackageDataBytes(intByte)
            package.extend(dataPackageBytes)

        # считаем и упаковывае crc
        crcPackageBytes = self._createCRCPackageBytes(package)
        package.extend(crcPackageBytes)

        return package

    def slaveCheckValidPackageAndCommand(self, address, package):
        print "Len Package: ", len(package)
        if len(package) > 3:
            startByte = ord(package[0])
            logging.debug("Type for package[1]: %s value: 0x%02x",
                          type(startByte),
                          startByte)

            # считаем сrc и сравниваем с тем, что получили
            receiveCrc = self._getDataFromBytes(
                    package[-2], package[-1])
            countCrcValue = self._countPackageCRC(package[:-2])

            if (receiveCrc != countCrcValue):
                logPackage.debug("Crc not equal! our count: %s | receive: %s",
                                 "0x{0:02x} {0}(0b{0:08b})".format(countCrcValue),
                                 "0x{0:02x} {0}(0b{0:08b})".format(receiveCrc))

                return False
            # определяем, что этот пакет нам
            if (ord(package[0]) != (0x80 + address)):
                logPackage.debug("Receive package start with: %s | Not for us (WrongAddress)",
                                 "0x{0:02x} {0}(0b{0:08b})".format(
                                    ord(package[0])))
                return False

            # определяем команду
            receiveCommand = self._getDataFromBytes(package[1], package[2])
            # if (receiveCommand != command):
            #     logPackage.debug("Receive package command code: %s | Not for us",
            #                      "0x{0:02x} {0}(0b{0:08b})".format(receiveCommand))
            #     return False
            print "receiveCommand: ", hex(receiveCommand)
            return receiveCommand
        return False
