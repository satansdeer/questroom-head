#!/usr/bin/python
# -*- coding: utf-8 -*-

 #!!! Надо добавить функции для получения значений, после посылки команд get
 #!!! Добавлять ведомого в список, даже при отсутсвии
# для этого добавить поле connection

# import random
import serial
# import time

# Для обработки очереди команд
import Queue
import threading

# Ведомое устройство
from spaceDevice import *
# Класс формирования пакета
# from spacePackage import *


class SpaceDeviceMaster:
    """Мастер устройств
    Запросы к устройствам собираются в FIFO очередь и выполняются
    последовательно.
    (стоит сделать поток для каждого com-порта - не реализовано)
     Содержит список ведомых устройств.

    Имена функций отправки команд на устройства начинаются с 'send*'
    Имена функций получения данных с 'get*', возвращают данные, полученные
        с устройств функциями 'send*'

    Список команд поддерживаемых каждым устройством:
    connectionCheck - проверка связи с устройством.
        Функция sendConnectionCheck()
        В ответ устройство возвращает "Hello!" и выставляется флаг
        connection на устройстве.
        Прочитать флаг можно функцией connection(<Имя узла или дескриптор>)
    setSimpleLEDs - установить значения простых светодиодов.
        Функция sendSetSimpleLEDs()
        Передаётся массив из 80 элементов со значениями 0 или 1.
        Если устройство подтвердило успешное получение команды,
        то массив сохраняется в объекте устройства и получить
        этот массив можно функцией getSimpleLEDS()
    setSmartLEDs - установить значения умных светодиодов.
        Функция sendSetSmartLEDs()
        Передаётся массив из 96 элементов. Каждый элемент принимает
        значения от 0 до 4095. Это яркость. 0 – не работает,
        4095 – самый яркий.
        getSmartLEDs()
    setLCD - установить значения для отображения на ЖКИ
        Функция sendSetLCD()
        Передаётся строка из 80 символов. Если строка больше 80,
        то она обрубается. Если меньше, то дополняется символом ' '.
    setRelays - установить значения реле.
        Функция sendSetRelays()
        Всего четыре реле. Массив из 4 элементов, значения 0 и 1

    getButtons - получить значения кнопок.
        Функция sendGetButtons()
        Предпочтительней использовать функцию getStuckButtons()
        Устройство возвращает массив из 18 элементов.
        1 - нажата. 0 - не нажата.
        Получить этот массив можно функцией getButtons()
        Лучше использовать команду getStuckButtons, так как
        она возвращает запомненные устройством нажатия на кнопки.
    getStuckButtons - получить значения "залипших" кнопок.
        Функция sendGetStuckButtons()
        Если кнопка была нажата, то устройство запоминает это состояние и не
        сбрасывает пока не придёт команда опроса состояния кнопок. Позволяет
        не пропустить быстрые нажатия из-за пауз при опросе.
        Получить массив также getButtons()
    getADC - получить значения слайдеров и резистивных крутилок
        с канала АЦП.
        Функция sendGetADC().
        Устройство возвращает массив из 8 элементов. Первый элемент
        соответствует нулевому каналу АЦП.
        Получить массив getADC()
    getEncoder - получить значения энкодеров (датчик угла поворота)
        Функция sendGetEncoders()
        Устройство возвращает массив из 4 элементов.
        getEncoders()
    getSensor - получить значения сенсоров. два элемента
        Функция sendGetSensors()
        getSensors()

    Устройства добаляются функцией addSlave()
    Информация необходимая для добавления устройства:
         1) символьное имя устройства для универсализации обращений
            к устройствам
         2) com-порт на котором устройство сидит, символьное обозначение
         3) адресс устройства в этом компорту
    Удалить устройство можно с помощью функции deleteSlave()
    """

    # Таймаут чтения com-порта, задаётся в секунах
    # Нужно учесть, что время ожидания ответа по протоколу
    # 300 мс с момента выдачи последнего байта посылки
    # COM_READ_TIMEOUT = None: ждать ответа вечно
    # COM_READ_TIMEOUT = 0: без блокировки по чтению
    # COM_READ_TIMEOUT = x: установить таймаут x секунд (можно float)
    COM_READ_TIMEOUT = .4
    # Таймаут по записи в com-порт
    COM_WRITE_TIMEOUT = 1
    # Остальные настройки com-порта в функции _initComPort()

    def __init__(self, queueSize=100):
        # список дескрипторов устройств
        self.__slaveList = []
        # список дескрипторов com-портов
        self.__comPortList = []

        # создаём очередь команд
        self.__commandQueue = Queue.Queue(queueSize)
        # создаём поток обработки Очереди команд
        commandQueueThread = threading.Thread(
            target=self._commandQueueThreadHandler)
        commandQueueThread.daemon = True
        commandQueueThread.start()

    def getQueueSize(self):
        return self.__commandQueue.qsize()

    # Функция потока обработки очереди комманд
    def _commandQueueThreadHandler(self):
        while True:
            slave, commad, data = self.__commandQueue.get()
            slave.sendCommand(commad, data)

    def addSlave(self, name, comPort, address):
        """
        При добалении нового устройства проверяется:
            1) инициализирован ли com-порт устройства.
            Если нет - идёт инициализация
            2) при успешной инициализации устройства - идёт обращение к нему
              по com-порту, посылается команда проверки связи.
            3) Если устройство не ответило на команду оно всё равно
                добавляется в список устройств.
        Проверить была ли установлена связь можно функцией
            self.connection()
        Повторить проверку соединения можно функцией
            self.sendConnectionCheck(slaveName),
                а потом self.connection(slaveName)
            либо напрямую функцию дескриптора устройства slave.connection()

        Параметры для добавления устройства:

        :param name: Универсальное символьное имя устройства для обращения.
        Для обращения также можно использовать возвращаемый дескриптор

        :param comPort:com-порт к которому подключено устройство,
        символьное обозначение в /dev. Например: /dev/usb0

        :param address: адрес устройства на этом com-порту

        :return: возвращается дескриптор созданного устройства

        """
        # Инициализируем com-порт
        comPortDescriptor = self._initComPort(comPort)

        # создаём ведомое устройство
        slave = SpaceDevice(address, comPortDescriptor, name)

        # проверям связь с устройством - шлем команду ConnectionCheck
        slave.sendConnectionCheck()
        self.__slaveList.append(slave)
        return slave

    def deleteSlave(self, slaveName):
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            self.__slaveList.remove(slave)
            return True
        return False

    def _initComPort(self, devComPortName):
        """Инициализация com-порта по символьному имени ser1
        или пути /dev/ser1.
        Возвращается дескриптор порта
        Исключения не обрабатываются.
        """
        # if comPort exist in list then return it
        for comPort in self.__comPortList:
            if comPort.name == devComPortName:
                return comPort

        # ComPort not exist in List ->
        #    then Open port, add in List and return
        serialDescriptor = serial.Serial(devComPortName, 9600,
                                         timeout=self.COM_READ_TIMEOUT,
                                         writeTimeout=self.COM_WRITE_TIMEOUT,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE)
        self.__comPortList.append(serialDescriptor)
        return serialDescriptor

    def _getSlaveDescriptor(self, slaveName):
        for slave in self.__slaveList:
            if isinstance(slaveName, SpaceDevice):
                if slave == slaveName:
                    return slave
            else:
                if slave.getName() == slaveName:
                    return slave
        return None

    def _putCommandInQueue(self, slaveName, command, data=None):
        """Добавление команды в очередь"""
        # получение дескриптора ведомого устройства
        slave = self._getSlaveDescriptor(slaveName)
        if not slave:
            print "Not Slave", slave
            return False
        # добавление команды в очередь
        queueData = [slave, command, data]
        self.__commandQueue.put(queueData)
        return True

    def sendConnectionCheck(self, slaveName):
        """Послать команду проверки соединения
        """
        return self._putCommandInQueue(slaveName, Command.connectionCheck)

    def sendSetSimpleLEDs(self, slaveName, data):
        """Послать команду установки простых светодиодов
        data должен быть массив из 80 значений 0 и 1
        """
        return self._putCommandInQueue(slaveName, Command.setSimpleLEDs, data)

    def sendSetSmartLEDs(self, slaveName, data):
        """Послать команду установки умных светодиодов
        96 светодиодов. В каждом по три значения от 0 до 255
        Итого: data - массив из 96 элементов со значениями от 0 до 4095
        Получить значения можно командой getSmartLEDs(slaveName)
        """
        slave = self._getSlaveDescriptor(slaveName)
        slave._saveSmartLEDs(data)
        return self._putCommandInQueue(slaveName, Command.setSmartLEDs, data)

    def sendSetSmartLEDs2(self, slaveName):
        """Послать команду установки умных светодиодов
        96 светодиодов. В каждом по три значения от 0 до 255
        Итого: data - массив из 96 элементов со значениями от 0 до 4095
        Получить значения можно командой getSmartLEDs(slaveName)
        """
        data = self.getSmartLEDs(slaveName)
        return self._putCommandInQueue(slaveName, Command.setSmartLEDs, data)

    def setSmartLEDs(self, slaveName, data):
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave._saveSmartLEDs(data)
        else:
            return None


    def sendSetLCD(self, slaveName, data):
        """Послать команду записи текста на LCD экран
        Массив не больше 80 символов;
        Правила формирования строк см. описание платы, протокола
        """
        return self._putCommandInQueue(slaveName, Command.setLCD, data)

    def sendSetRelays(self, slaveName, data):
        """# Установка значений реле
        4 штуки; массив из четырёх элементов
        """
        return self._putCommandInQueue(slaveName, Command.setRelays, data)

    def sendGetButtons(self, slaveName):
        """Послать команду получение значений кнопок
        Лучше использовать команду GetStuckButtons (ниже)
        При интенсивной загрузке платы командами возможна ситуация, когда
        кнопка была нажата, потом отпущена, а команда опроса пришла позже,
        получается нажатие может быть не зафиксировано.
        """
        return self._putCommandInQueue(slaveName, Command.getButtons)

    def sendGetStuckButtons(self, slaveName):
        """Послать команду получения залипших кнопок
        Лучше чем sendGetButtos, т.к. позволяет получить все нажатые
        кнопки за время после последне опроса.
        """
        return self._putCommandInQueue(slaveName, Command.getStuckButtons)

    def sendGetADC(self, slaveName):
        """Получить значения слайдеров, крутилок, всего что сидит
        на каналах АЦП
        в ответ 8 значений от 0 до 255
        Данные сохраняются в массиве ведомого
        Получить их можно командой getADC(slaveName)
        """
        return self._putCommandInQueue(slaveName, Command.getADC)

    def sendGetEncoders(self, slaveName):
        """Послать команду получения значений энкодеров: 4 значения"""
        return self._putCommandInQueue(slaveName, Command.getEncoder)

    def sendGetSensors(self, slaveName):
        """Послать команду получения значений умных светодиодов"""
        return self._putCommandInQueue(slaveName, Command.getSensor)

    # Геттеры данных устройств
    def getSimpleLEDs(self, slaveName):
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getSimpleLEDs()
        else:
            return None

    def getSmartLEDs(self, slaveName):
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getSmartLEDs()
        else:
            return None

    def getButtons(self, slaveName):
        """Возвращает как значения залипших так и просто прочитанных кнопок"""
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getButtons()
        else:
            return None

    def getRelays(self, slaveName):
        """Возвращает значения четрых реле"""
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getRelays()
        else:
            return None

    def getADC(self, slaveName):
        """Возвращает значения слайдеров и крутилок с АЦП"""
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getADC()
        else:
            return None

    def getEncoders(self, slaveName):
        """Возвращает значения энкодеров (крутилок); 4"""
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getEncoders()
        else:
            return None

    def getSensors(self, slaveName):
        """Возвращает значение сенсоров"""
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.getSensors()
        else:
            return None

    def connection(self, slaveName):
        slave = self._getSlaveDescriptor(slaveName)
        if slave:
            return slave.connection()
        else:
            return None


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    master = SpaceDeviceMaster()
    master.addSlave("simSlave1", "./ptyp1", 1)
    master.sendConnectionCheck("simSlave1")
