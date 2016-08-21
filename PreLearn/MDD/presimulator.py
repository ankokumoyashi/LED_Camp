# coding: UTF-8
'''
Created on 2016/07/01
@author: okayama
PreCreate2の動作を模擬する

'''
from __future__ import print_function
import random

class PreSimulator:
    def __init__(self):
        self.velocity = 0
        self.radius = 0
        self.distance = 0
        self.angle = 0

    def drive(self, velocity, radius):
        self.velocity = velocity
        self.radius = radius

    def get_bump(self):
        work = random.randint(0,500)
        if work == 1 :
            bumpsWheeldrops = 1
            self.velocity = 0
            self.radius = 0
            print("bump Left!")
        elif work == 2 :
            bumpsWheeldrops = 2
            self.velocity = 0
            self.radius = 0
            print("bump Right!")
        elif work == 3 :
            bumpsWheeldrops = 4
            self.velocity = 0
            self.radius = 0
            print("bump Center!")
        else :
            bumpsWheeldrops = 0

        return bumpsWheeldrops

    def get_distance(self):
        return self.distance

    def get_angle(self):
        return self.angle

    def update(self):
        if self.radius == 0 : self.distance += self.velocity
        elif self.radius > 0 : self.angle += self.velocity
        elif self.radius < 0 : self.angle -= self.velocity


