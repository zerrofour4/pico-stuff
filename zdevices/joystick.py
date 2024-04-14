import time, math
from machine import Pin, PWM, ADC

class Joystick:
    
    def __init__(self, x_n, y_n, center = 33000, dz_slop=500):
        
        self.x_axis = ADC(Pin(x_n))
        self.y_axis = ADC(Pin(y_n))
        self.input_mapping = { "x" : self.x_axis, "y": self.y_axis}
        self.dz_slop = dz_slop
        self.center = center
    
    def read_axis(self, axis):
        try:
            p = self.input_mapping[axis]
            return p.read_u16()
        except KeyError:
            print(axis + "not implemented or invalid input id")
            return None
        
    def read_axis_for_motor(self, axis, percentage=False):
        try:
            p = self.input_mapping[axis]
        except KeyError:
            print(axis + "not implemented or invalid input id")
            return None
        raw = p.read_u16()
        position = self.center - raw
        direction = 0
        if position > self.dz_slop:
            direction = 2
        elif position < (0 - self.dz_slop):
            direction = 1
        ap = abs(position)
        if ap < self.dz_slop:
            ap = 0
        if percentage:
            return int(math.floor((ap/32535) * 100)), direction
        return ap, direction
        
            