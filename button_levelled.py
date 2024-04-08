import machine
import time
import random



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
        


def _write_random(reg):
    print("pressed")
    data = random.randint(0, 127)
    reg.write(data)

def _replay_irq(reg):
    reg.replay_last_data()

if __name__ == "__main__":
    num = 0
    reg = ShiftRegister(0, 1, 2)
    green_b = Button(15)
    blue_b = Button(14)
    
    reg.write(0)
    while True:
        
        if green_b.read() == 1:
            _write_random(reg)
        elif blue_b.read() == 1:
            reg.replay_last_data()
            reg.write(0)
            
