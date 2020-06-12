
import keyboardInput as KB

''' Class can be controlled by the controller
    and functions map to what controller can do
    on button press
'''

class Context:

    def __init__(self):
        # commands
        self.commands = {KB.A:self.doA,KB.B:self.doB,KB.X:self.doX,KB.Y:self.doY,KB.DOWN:self.doDOWN, \
                                        KB.UP:self.doUP,KB.LEFT:self.doLEFT,KB.RIGHT:self.doRIGHT,KB.L:self.doL, \
                                        KB.R:self.doR,KB.START:self.doSTART, KB.SELECT:self.doSELECT}


    # virtual functions to be defined by sub classes

    def doA(self):
        pass
    def doB(self):
        pass
    def doX(self):
        pass
    def doY(self):
        pass
    def doLEFT(self):
        pass
    def doRIGHT(self):
        pass
    def doUP(self):
        pass
    def doDOWN(self):
        pass
    def doL(self):
        pass
    def doR(self):
        pass
    def doSTART(self):
        pass
    def doSELECT(self):
        pass

