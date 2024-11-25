import dht
import machine

class ZDHT11:
    def __init__(self, pin, temperature_unit="c"):
        self.sensor = dht.DHT11(machine.Pin(pin))
        self.temperature_unit = temperature_unit
        
    def measure(self):
        self.sensor.measure()
        temperature = self.sensor.temperature()
        if self.temperature_unit == "f":
            temperature = int((temperature * 1.8) + 32)
        return temperature, self.sensor.humidity()
        