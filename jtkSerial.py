import json
from json import JSONDecoder    
import select
class jtkSerial:

    import usbmux
    import SocketServer

    from optparse import OptionParser
    import sys
    import threading
    import struct
    import Queue
    from collections import OrderedDict


    from jtkHVAC import jtkHVAC
    from jtkSchedule import jtkSchedule


    hvac = any
    sched = any
    
    mux = any
    psock = any
    outGoingMsgQueue = Queue.Queue()
    
    def __init__(self):
        print "intialzing Serial Communication"
        self.dispatchFunctionDict = {'setSchedule': self.setSchedule,
                                'getSchedule': self.getSchedule,
                                'getTemp': self.getTemp,
                                'setTemp': self.setTemp, #used for demo in absence of temp sensor
                                'setDate': self.setDate,
                                'setSetPoint': self.setSetPoint,
                                'bigSend': self.bigSend}
        
        self.replyDict = {'setSchedule': 'setSchedule',
                          'getSchedule': 'getSchedule',
                          'getTemp': 'getTemp',
                          'setTemp': 'setTemp',
                          'setDate': 'setDate',
                          'setSetPoint': 'setSetPoint'}

    def scanForDevice(self):
        print "Looking for devices..."
        try:
            self.mux = self.usbmux.USBMux()
        except:
            print "no device"
            return False
        if not self.mux.devices:
            self.mux.process(1.0)
        if not self.mux.devices:
            print "No device found"
            return False
        else:
            print "scan return true"
            return True

    def connectToDevice(self):
        dev = self.mux.devices[0]
        print "connecting to device %s" % str(dev)
        try:
            self.psock = self.mux.connect(dev, 2345)
        except:
            print "connect fail"
            return False
        return True

    def readWriteControl(self, hvac, sched):
        self.hvac = hvac
        self.sched = sched
        
        isConnected = True
        counter = 0
        while isConnected:
            ready = select.select([self.psock], [], [], 1)

            if ready[0]:
                msg = self.psock.recv(20000)
            
                if not msg:
                    isConnected = False
                else:
                    print msg
                    print "message Read"
                    self.dispatchMessage(msg)
            try:
                if(not self.outGoingMsgQueue.empty()):
                    print "sending message"
                    outMsg = self.outGoingMsgQueue.get()
                    self.psock.send(outMsg)
                    print "SENT!:" + outMsg #@@ debug
            except Exception, e:
                print "sendFail: " + str(e)
                isConnected = False

            #updates HVAC controls every second?
            self.hvac.controlUpdate(sched)

        return isConnected
            

    def closeConnection(self):
        psock.close()

    def dispatchMessage(self, msg):

        msgObj =  json.JSONDecoder(object_pairs_hook=self.OrderedDict).decode(msg)
#        msgObj = {'type': 'setSetPoint', 'setPoint':58} #@@debug 
        #each message type maps to a dispatch function 
        if type(msgObj) is self.OrderedDict:
            #checks if the msgObj has a field 'type' or the type in that field
            # matches any defined function
            if self.dispatchFunctionDict.get(msgObj.get('type', None), None):
                self.dispatchFunctionDict[msgObj['type']](msgObj)
            else:
                print "improperly formatted dictionary object"
        else:
            print "unknown message: " + msg

    def bigSend(self,msgObj):
        print "bigSend"
        self.outGoingMsgQueue.put('{"obj": {"Friday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}], "Tuesday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 6, "type": "getSchedule"}8, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}], "Thursday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}], "Monday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}], "Saturday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}], "Wednesday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}], "Sunday": [{"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}, {"temp": 68, "status": "Home"}]}')
    def setSchedule(self, msgObj):
        print "setSchedule"
        self.sched.setScheduleDict(msgObj['schedule'])
        #self.sched.printSchedule() #@@debug print
        
    #gets current schedule upon request to be sent on the serial bus
    def getSchedule(self, msgObj):
        print "getSchedule"

        res = self.constructReplyJson(msgObj['type'], self.sched.scheduleDict)
        self.outGoingMsgQueue.put(res)
    
    #gets the current temperature to be sent on the serial bus
    def getTemp(self, msgObj):
        print "getTemp"
        temp = self.hvac.getTemp()
        res = self.constructReplyJson(msgObj['type'], temp)
        self.outGoingMsgQueue.put(res)

    def setTemp(self, msgObj):
        print "setTemp"
        self.hvac.setTemp(msgObj['temp'])

    def setDate(self, msgObj):
        print "setDate"
        dtDHMS = msgObj['datetime']
        self.sched.setTime(dtDHMS[0], dtDHMS[1], dtDHMS[2], dtDHMS[3])

    def setSetPoint(self, msgObj):
        print "setSetPoint"
        setPoint = msgObj['setPoint']
        self.hvac.setSetPoint(setPoint)
        self.sched.setTimeSegment(self.sched.getTime(), setPoint)
        

    #constructs a json string reply
    #takes the request object whose 'type' is used to find the proper
    #return 'type', and the object is added to the appropriate object field
    def constructReplyJson(self, reqType, resJson):
        respType = self.replyDict[reqType]

        response = {'type':respType, 'obj': resJson}
        return json.dumps(response, sort_keys=False)
