# coding: UTF-8
'''
Created on 2016/07/01
@author: hosoai
@author: okayama
センサ監視用スレッド
intervalで指定したmsごとに全センサ値を要求する．
取得したセンサ値は保持し，前回取得した値と比較，
差分が合った場合は，リスナー登録されている関数に通知する．
'''
from __future__ import print_function
import threading
import time
import math

from sensor import Sensor
from sensor import Event

ENC_TO_DISTANCE = 72 * math.pi / 508.8 # タイヤ径72mm * Pi / 一周エンコーダ数 ：理論値なので，実計測で調整すること．
WHEEL_BASE = 117.5

class Observer(threading.Thread):
    def __init__(self, sim, interval):
        super(Observer, self).__init__()
        self.interval = interval
        self.running = True
        self.sensor = Sensor()
        self.prevSensor = None
        self.sim = sim
        self.listeners = []
        self.leftEncoder = 0
        self.rightEncoder = 0
        self.totalDistance = 0
        self.totalAngle = 0
        self.nextDistance=None
        self.nextDistanceCompare=None
        self.nextAngle=None
        self.nextAngleCompare=None
        self.daemon = True

    def add_listener(self, listener):
        self.listeners.append(listener)

    def stop(self):
        self.running = False

    def get_distance(self):
        return self.totalDistance
    def get_angle(self):
        return self.totalAngle

    def _request_sensor(self):
        self.sensor.get_sensor(self.sim)

    def set_next_distance(self, distance, greater=True):
        self.nextDistance = self.totalDistance + distance
        self.nextDistanceCompare = greater

    def set_next_angle(self, angle, greater=True):
        self.nextAngle = self.totalAngle + angle
        self.nextAngleCompare = greater

    def _raise_event(self, eventList):
        for listener in self.listeners:
            listener(eventList)

    def run(self):
        while(self.running):
            self._request_sensor()
            self.sim.update()

            self.totalDistance = self.sim.get_distance()
            self.totalAngle = self.sim.get_angle()

            print("Distance:" + str(self.totalDistance) + " Angle:" + str(self.totalAngle))

            if self.prevSensor :
                eventList = self.sensor.diff(self.prevSensor)
                if (eventList and len(eventList)>0):
                    self._raise_event(eventList)

                # check reachDistance Event
                if(self.nextDistance):
                    if(self.nextDistanceCompare):
                        if(self.totalDistance>=self.nextDistance):
                            self.nextDistance=None
                            self.nextDistanceCompare=None
                            self._raise_event([Event.reachDistance])
                            #print "raise reachDistance1"
                    else:
                        if(self.totalDistance<=self.nextDistance):
                            self.nextDistance=None
                            self.nextDistanceCompare=None
                            self._raise_event([Event.reachDistance])
                            #print "raise reachDistance2"

                # check reachAngle Event
                if(self.nextAngle):
                    if(self.nextAngleCompare):
                        if(self.totalAngle>=self.nextAngle):
                            self.nextAngle=None
                            self.nextAngleCompare=None
                            self._raise_event([Event.reachAngle])
                    else:
                        if(self.totalAngle<=self.nextAngle):
                            self.nextAngle=None
                            self.nextAngleCompare=None
                            self._raise_event([Event.reachAngle])
            self.prevSensor = self.sensor
            time.sleep(self.interval/1000.0)
