# Example using PWM to fade an LED.

import time
from machine import Pin, PWM, ADC

def fade(pwm):
  # Fade the LED in and out a few times.
  duty = 0
  direction = 1
  for _ in range(8 * 256):
      duty += direction
      if duty > 255:
          duty = 255
          direction = -1
      elif duty < 0:
          duty = 0
          direction = 1
      pwm.duty_u16(duty * duty)
      time.sleep(0.001)



class Motor:
    
    def __init__(self, enable_n, forward_n, reverse_n, PWMFreq = 2000):
        
        
        self.forward_pin = machine.Pin(forward_n, Pin.OUT)
        self.reverse_pin = machine.Pin(reverse_n, Pin.OUT)
        self.enable_pin = machine.Pin(enable_n, Pin.OUT)
        self.enable_pwm = machine.PWM(self.enable_pin)
        
        self.enable_pwm.freq(PWMFreq)
        self.enable_pwm.duty_u16(0)
        
    
    def Forward(self, speed):
        PWM = int(speed * 655.35)
        self.forward_pin.on()
        self.reverse_pin.off()
        self.enable_pwm.duty_u16(PWM)
        print(PWM)
    
    def Reverse(self, speed):
        PWM = int(speed * 655.35)
        self.reverse_pin.on()
        self.forward_pin.off()
        self.enable_pwm.duty_u16(PWM)

    
    def Stop(self):
        self.forward_pin.off()
        self.reverse_pin.off()
        self.enable_pwm.duty_u16(0)

        
        

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


if __name__ == "__main__":
    
    motor = Motor(0,16, 17)
    js = Joystick(27, 26)
    
    
    while True:
        pos = js.read_axis("x")
        print("x" + str(pos))
        pos = js.read_axis("y")
        print("y" + str(pos))

        new_speed = int((pos/65535) * 100) - 52
        print(str(new_speed))
        time.sleep(0.05)
        if new_speed > 0:
          motor.Forward(new_speed)
        elif new_speed < -3:
            motor.Reverse(abs(new_speed))
        else:
            motor.Stop()


        #time.sleep(100)


        