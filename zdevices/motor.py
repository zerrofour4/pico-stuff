import machine
import time
import random

class Motor:
    
    def __init__(self, enable_n, forward_n, reverse_n, PWMFreq = 2000):
        
        
        self.forward_pin = machine.Pin(forward_n, machine.Pin.OUT)
        self.reverse_pin = machine.Pin(reverse_n, machine.Pin.OUT)
        self.enable_pin = machine.Pin(enable_n, machine.Pin.OUT)
        self.enable_pwm = machine.PWM(self.enable_pin)
        
        self.enable_pwm.freq(PWMFreq)
        self.enable_pwm.duty_u16(0)
        self.Stop()
        
    
    def Forward(self, speed):
        PWM = int(speed * 655.35)
        self.forward_pin.on()
        self.reverse_pin.off()
        self.enable_pwm.duty_u16(PWM)
    
    def Reverse(self, speed):
        PWM = int(speed * 655.35)
        self.reverse_pin.on()
        self.forward_pin.off()
        self.enable_pwm.duty_u16(PWM)

    
    def Stop(self):
        self.forward_pin.off()
        self.reverse_pin.off()
        self.enable_pwm.duty_u16(0)

        