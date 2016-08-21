from __future__ import print_function
from sensor import Event
from main import preCreate2
from precreate2 import PreCreate2

class Controller :
    def __init__(self):
        self.cnt = 0
        self.stateMap = {
            "FORWARD":{
                "entry": "print(\"FORWARD\")\npreCreate2.set_next_distance(1000)",
                "do"   : "preCreate2.drive(100,0)",
                "exit" : "",
                Event.reachDistance : {
                    "guard": (lambda : (self.cnt < 4)),
                    "act"  : "",
                    "next" : "TURN"
                },
                Event.pushBumperLeft : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "BACK"
                },
                Event.pushBumperRight : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "BACK"
                },
                Event.pushBumperCenter : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "BACK"
                },
            },
            "TURN":{
                "entry": "print(\"TURN\")\npreCreate2.set_next_angle(90)",
                "do"   : "preCreate2.drive(100,1)",
                "exit" : "",
                Event.reachAngle : {
                    "guard": (lambda : True),
                    "act"  : "self.cnt = self.cnt + 1",
                    "next" : "FORWARD"
                },
                Event.pushBumperCenter : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "BACK"
                },
                Event.pushBumperRight : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "BACK"
                },
                Event.pushBumperLeft : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "BACK"
                },
            },
            "BACK":{
                "entry": "print(\"BACK\")\npreCreate2.set_next_distance(-200)",
                "do"   : "preCreate2.drive(-100,0)",
                "exit" : "",
                Event.reachDistance : {
                    "guard": (lambda : True),
                    "act"  : "",
                    "next" : "FORWARD"
                },
            },
        }
        self.current = self.stateMap["FORWARD"]
        self.initState()

    def initState(self):
        exec(self.current["entry"])
        exec(self.current["do"])

    def doTransition(self, event):
        state = self.current
        if event in state:
            trans = state[event]
            if trans["guard"]():
                exec(state["exit"])
                exec(trans["act"])
                state = self.stateMap[trans["next"]]
                exec(state["entry"])
                exec(state["do"])
                self.current = state

