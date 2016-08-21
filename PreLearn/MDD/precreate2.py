# coding: UTF-8
'''
Created on 2016/07/01
@author: hosoai
@author: okayama
事前実習用ライブラリのメインクラス．主にこのクラスから操作を行う．
'''
import struct
import time

from sensor import Sensor
from observer import Observer
from presimulator import PreSimulator

# create2 tuning parameters

class PreCreate2(object):
    __instance = None
    def __new__(cls, *args, **keys):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **keys)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, threading=False, interval=500):
        if (self.__instance.__initialized): return
        self.__instance.__initialized = True
        time.sleep(2)

        self.sim = PreSimulator()

        if threading:
            self.observer = Observer(self.sim, interval)
            self.observer.start()
        time.sleep(1)

    def drive(self, velocity, radius):
        self.sim.drive(velocity, radius)

# for multithread
    def get_distance(self):
        return self.observer.get_distance()

    def get_angle(self):
        return self.observer.get_angle()

    def add_event_listener(self, listener):
        self.observer.add_listener(listener)

    def set_next_distance(self, distance):
        if distance >= 0 : greater = True
        else : greater = False
        self.observer.set_next_distance(distance, greater)

    def set_next_angle(self, angle):
        if angle >= 0 : greater = True
        else : greater = False
        self.observer.set_next_angle(angle, greater)
