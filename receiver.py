from zdevices import shift_register
import struct
import utime
from machine import Pin, SPI
from nrf24l01 import NRF24L01

spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
cfg = {"spi": spi, "csn": 9, "ce": 13}
rx_pipe = b"\xe1\xf0\xf0\xf0\xf0"
tx_pipe = b"\xd2\xf0\xf0\xf0\xf0"

def radio():
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size=32)

    nrf.open_tx_pipe(tx_pipe)
    nrf.open_rx_pipe(1, rx_pipe)
    nrf.start_listening()
    return nrf

if __name__ == "__main__":
    reg = shift_register.ShiftRegister(0, 1, 2)
    reg.write(0)

    radio = radio()
    data_format = "i"
    num_leds = 0
    while True:          
      if radio.any():
          while radio.any():
              buf = radio.recv()
              num_leds = struct.unpack("i", buf)
              print(num_leds)
          reg.fill(num_leds[0])
        


