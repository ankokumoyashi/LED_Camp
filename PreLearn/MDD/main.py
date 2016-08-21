
#!/usr/bin/python
from precreate2 import PreCreate2
import time
import Controller

preCreate2 = PreCreate2(threading=True)

controller = None

def event_handler(events):
    for e in events:
        controller.doTransition(e)

if __name__ == '__main__':
    controller = Controller.Controller()
    preCreate2.add_event_listener(event_handler)
    while True:
        time.sleep(1)
