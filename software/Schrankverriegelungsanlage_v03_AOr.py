#import RPi.GPIO as GPIO
import datetime
import time
import json

#Defining classes
class ClockChannel():
    id = ""
    def __init__(self, id, givenTimeUnlock, givenTimeLock):
        self.id = id
        self.givenTimeUnlock = givenTimeUnlock
        self.givenTimeLock = givenTimeLock
        currentTimeSecOfDay = 0
        givenTimeUnlockSecOfDay = 0
        givenTimeLockSecOfDay = 0
        self.channelStatus = False
    def compareTime(self):
        #print('beginn')
        currentTimeSecOfDay = (datetime.datetime.now().hour * 3600) + (datetime.datetime.now().minute * 60) + datetime.datetime.now().second
        givenTimeUnlockSecOfDay = (self.givenTimeUnlock.hour * 3600) + (self.givenTimeUnlock.minute * 60) + self.givenTimeUnlock.second
        givenTimeLockSecOfDay = (self.givenTimeLock.hour * 3600) + (self.givenTimeLock.minute * 60) + self.givenTimeLock.second    
        if (currentTimeSecOfDay >= givenTimeUnlockSecOfDay) and (currentTimeSecOfDay < givenTimeLockSecOfDay):
            #print('unlock')
            self.channelStatus = True
            return True
        else:
            #self.channelStatus = False
            return False

class Timer():
    id = ""
    channels = []
    def __init__(self, id):
        self.id = id
 
    def addChannel(self,ClockChannel):
        print('added')
        self.channels.append(ClockChannel)
        
class Lock():
    id = ""
    #logicalState = 
    def __init__(self,id):
        self.id = id
        self.logicalState = False
        self.controlSpoilStateLock = False
        self.controlSpoilStateUnlock = False
    def changeState(self,boolState):
        if boolState == False:
            print("locking changeState")
            self.controlSpoilStateLock=True
            time.sleep(0.5)
            self.controlSpoilStateLock=False
            self.logicalState = False
        elif boolState == True:
            print("unlocking changeState")
            self.controlSpoilStateUnlock=True
            time.sleep(0.5)
            self.controlSpoilStateUnlock=False
            self.logicalState = True    
        
#Instanciating classes to objects. Timer gets Clockchannels, Clockchannel gets start and end time. Lock ist separately.
timer1=Timer(1)
timer1.addChannel(ClockChannel(0, givenTimeUnlock=datetime.time(9, 24, 0), givenTimeLock=datetime.time(10, 0, 30)))
timer1.addChannel(ClockChannel(1, givenTimeUnlock=datetime.time(11, 15, 0), givenTimeLock=datetime.time(12, 30, 0)))
timer1.addChannel(ClockChannel(2, givenTimeUnlock=datetime.time(23, 32, 0), givenTimeLock=datetime.time(23, 33, 0)))
lock1=Lock(0)

with open('lockingUnlockingTimes_json.txt', 'r') as infile:
    #print (infile.read())
    jsonChannelObject = json.load(infile)
    print(jsonChannelObject)
    print (jsonChannelObject['jsonDataName'])
    print (jsonChannelObject['channels']['channel'][0]['name'])
    print (jsonChannelObject['channels']['channel'][1]['name'])

"""
with open('lockingUnlockingTimes_json.txt', 'r') as infile:
    #person = '{"name": "Bob", "languages": ["English", "Fench"]}'
    person_dict = json.load(infile)

    # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
    print( person_dict)

    # Output: ['English', 'French']
    print(person_dict['languages'])
"""

# Endless loop
while True:
    time.sleep(1) #cycle time
    #print(datetime.datetime.now())
    #print (lock1.logicalState)
    #print(timer1.channels[0].channelStatus)
    if lock1.logicalState==False: #if lock is locked
        for i in range(len(timer1.channels)):
            #print (i)
            if (timer1.channels[i].compareTime() == True): #if time channel 0 is to be unlocked and lock 
                print("Timer Breakfast condition to unlock")
                print (lock1.logicalState)
                lock1.changeState(True)
                
    else: #if lock is unlocked
        for i in range(len(timer1.channels)):
            #print (i)
            if (timer1.channels[i].compareTime() == False) and (timer1.channels[i].channelStatus == True): #if time channel 0 is to be locked and the same channel currently unlocked  
                print("Timer Breakfast condition to lock")
                lock1.changeState(False)
                timer1.channels[i].channelStatus = False
                
            else:
                print("do nothing") 
    
