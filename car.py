from zdevices import shift_register, motor
import struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01

spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cfg = {"spi": spi, "csn": 9, "ce": 13}
rx_pipe = b"\xe1\xf0\xf0\xf0\xf0"
tx_pipe = b"\xd2\xf0\xf0\xf0\xf0"

def start_radio():
    csn = Pin(cfg["csn"], mode=machine.Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=machine.Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size=4)

    nrf.open_tx_pipe(tx_pipe)
    nrf.open_rx_pipe(1, rx_pipe)
    nrf.start_listening()
    return nrf

if __name__ == "__main__":

    r_started = False
    while r_started is False:
        try:
            radio = start_radio()
            r_started = True
        except Exception as e:
            utime.sleep(1)
            print(e)
    
    right = motor.Motor(16, 18, 17)
    left = motor.Motor(19, 21, 20)
    
    right.Forward(40)
    left.Reverse(40)
    utime.sleep(.15)

    left.Stop()
    right.Stop()
    while True:
    
        if radio.any():
          while radio.any():
              buf = radio.recv()
              print(buf)
              (direction, l_speed, r_speed,) = struct.unpack("iii", buf)
          
              if direction == 1:
                  right.Forward(r_speed)
                  left.Forward(l_speed)
              if direction == 2:
                  right.Reverse(r_speed)
                  left.Reverse(l_speed)
        
        




