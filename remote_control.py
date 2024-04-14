from zdevices import button, joystick
import struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01

spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cfg = {"spi": spi, "csn": 9, "ce": 13}
tx_pipe = b"\xe1\xf0\xf0\xf0\xf0"
rx_pipe = b"\xd2\xf0\xf0\xf0\xf0"

def radio():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size=16)

    nrf.open_tx_pipe(tx_pipe)
    nrf.open_rx_pipe(1, rx_pipe)
    #nrf.start_listening()
    return nrf

def send(l_direction, r_direction, l_speed,r_speed):
    try:
        radio.stop_listening()
        d = struct.pack("iii", direction, l_speed, r_speed)
        print("will send: " + str(d))
        radio.send(struct.pack("iiii", l_direction, r_direction, l_speed, r_speed))
    except OSError as e:
        print("fail send")
    radio.start_listening()

if __name__ == "__main__":

    #red = button.Button(16,"red")
    #yellow = button.Button(17,"yellow")
    
    #buttons = [red, yellow]
    
    joystick = joystick.Joystick(26, 27, dz_slop=500)
    
    radio = radio()
    while True:
        l_speed = 0
        r_speed = 0
        direction = 0

        utime.sleep(.1)
        x, x_dir = joystick.read_axis_for_motor("x", True)
        y, y_dir = joystick.read_axis_for_motor("y", True)
        
        if y_dir > 0 and x_dir == 0: #forward or backwards
            send(y_dir, y_dir, y,y)
        elif x_dir == 1: #right turn
            send(1, 2, x, x)
        elif x_dir == 2: # left turn
            send(2, 1, x, x )
            
        else:
            send(0, 0, 0, 0)
        utime.sleep(.05)

        

          
        
                




