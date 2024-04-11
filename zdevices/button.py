import machine


class Button:
    def __init__(self, p_n, label, callback=None):
        self.b_pin = machine.Pin(p_n, machine.Pin.IN)
        if callback:
            self.b_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)
        self.label = label
        
    def read(self):
        return self.b_pin.value()