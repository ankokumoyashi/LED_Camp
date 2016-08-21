# coding: UTF-8
'''
Created on 2016/07/01
@author: hosoai
@author: okayama
センサ用構造体
全センサデータ（PacketID100）で得られる80Byteのバイト列を
この構造体にキャストする．（genFromBytes参照）
'''

from presimulator import PreSimulator

class Sensor:

    def __init__(self):
        self.bumpsWheeldrops = 0
        self.buttons = 0

    def get_sensor(self, sim):
        self.bumpsWheeldrops = sim.get_bump()

    def diff(self, other):
        eventList = []
        # if self.bumpsWheeldrops != other.bumpsWheeldrops :
        if self.bumpsWheeldrops & 1 : eventList.append(Event.pushBumperLeft)
        if self.bumpsWheeldrops & 2 : eventList.append(Event.pushBumperRight)
        if self.bumpsWheeldrops & 4 : eventList.append(Event.pushBumperCenter)
        if self.buttons != other.buttons : eventList.append(Event.changeButtons)

        return eventList

class Event(enumerate):
    changeButtons = 12
    reachDistance = 53
    reachAngle = 54
    pushBumperLeft = 56
    pushBumperCenter = 57
    pushBumperRight = 58
