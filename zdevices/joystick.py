import time
from machine import Pin, PWM, ADC

class Joystick:
    
    def __init__(self, x_n, y_n):
        
        self.x_axis = ADC(Pin(x_n))
        self.y_axis = ADC(Pin(y_n))
        self.input_mapping = { "x" : self.x_axis, "y": self.y_axis}
    
    def read_axis(self, axis):
        try:
            p = self.input_mapping[axis]
            return p.read_u16()
        except KeyError:
            print(axis + "not implemented or invalid input id")
            return None