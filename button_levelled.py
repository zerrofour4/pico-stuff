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
        


class Button:
    def __init__(self, p_n, callback=None):
        self.b_pin = machine.Pin(p_n, machine.Pin.IN)
        if callback:
            self.b_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
        
    def read(self):
        return self.b_pin.value()
        

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
        


def _write_random(reg):
    print("pressed")
    data = random.randint(0, 255)
    reg.write(data)

def _replay_irq(reg):
    reg.replay_last_data()


def button_listen():
    global reg
    global green_b
    global blue_b
    while True:
        
        if green_b.read() == 1:
            _write_random(reg)
        elif blue_b.read() == 1:
            reg.replay_last_data()
            reg.write(0)
            

def us_measure():
    global us
    global reg
    while True:
        d = us.measure()
        print(d)
        if d > 255:
            ld = 255
        else:
            ld = int(d)
        num_led = msb(ld)
        if num_led < 0:
            num_led = 0
        d = (0b11111111>>num_led)
        reg.write(d)
        print(d)
        time.sleep_ms(200)


def msb(n):
    ndx = 0
    while ( 1 < n ):
      n = ( n >> 1 )
      ndx += 1
 
    return ndx


if __name__ == "__main__":
    num = 0
    reg = ShiftRegister(0, 1, 2)
    green_b = Button(13)
    blue_b = Button(12)
    internal_led = machine.Pin("LED", machine.Pin.OUT)
    reg.write(0)
    us = UltraSonic(14, 15)
    
    _thread.start_new_thread(us_measure,())
    while True:
        internal_led.toggle()
        time.sleep(1)