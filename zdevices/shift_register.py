import machine
import time
import random
import _thread
import utime

class ShiftRegister:
    
    def __init__(self, sdi_n, rclk_n, srclk_n, replay_ms = 100):
        
        self.sdi = machine.Pin(sdi_n, machine.Pin.OUT)
        self.rclk = machine.Pin(rclk_n, machine.Pin.OUT)
        self.srclk = machine.Pin(srclk_n, machine.Pin.OUT)
        self.last_data = list()
        self.replay_ms = replay_ms
    
    def _append_last(self, data):
        if len(self.last_data) == 20:
            self.last_data.pop(0)
        self.last_data.append(data)
    
    def write(self, data, update_last = True):
        self.rclk.low()
        time.sleep_ms(5)
        for bit in range(7, -1, -1):
            self.srclk.low()
            time.sleep_ms(5)
            value = 1 & (data >> bit)
            self.sdi.value(value)
            time.sleep_ms(5)
            self.srclk.high()
            time.sleep_ms(5)
        time.sleep_ms(5)
        self.rclk.high()
        time.sleep_ms(5)
        if update_last:
            self._append_last(data)
    
    def replay_last_data(self):
        for d in self.last_data:
            self.write(d, False)
            print("{:0>8b}".format(d))
            time.sleep_ms(self.replay_ms)
            
            
    def fill(self, num=8):
        d = 0 | (0b11111111>>(8- num))
        print("{:0>8b}".format(d))
        self.write(d)