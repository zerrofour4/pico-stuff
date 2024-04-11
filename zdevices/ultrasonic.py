import machine
import time
import random
import utime

class UltraSonic:
    
    def __init__(self, trig_n, echo_n):
        self.trig_pin = machine.Pin(trig_n, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_n, machine.Pin.IN)

    def measure(self):
        self.trig_pin.low()
        time.sleep_us(2)
        self.trig_pin.high()
        time.sleep_us(10)
        self.trig_pin.low()
        while not self.echo_pin.value():
            pass
        time1 = time.ticks_us()
        while self.echo_pin.value():
            pass
        time2 = time.ticks_us()
        duration = time.ticks_diff(time2,time1)
        return duration * 340 / 2 / 10000