from zdevices import button
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
    nrf = NRF24L01(spi, csn, ce, payload_size=4)

    nrf.open_tx_pipe(tx_pipe)
    nrf.open_rx_pipe(1, rx_pipe)
    #nrf.start_listening()
    return nrf

if __name__ == "__main__":

    red = button.Button(16,"red")
    yellow = button.Button(17,"yellow")
    
    buttons = [red, yellow]
    
    radio = radio()
    num_leds = 0
    while True:
        print(num_leds)

        try:
            radio.stop_listening()
            radio.send(struct.pack("i", num_leds))
        except OSError:
            print("fail send")
        radio.start_listening()
        num_leds += 1
        if num_leds > 8:
            num_leds = 0
        utime.sleep(.13)


