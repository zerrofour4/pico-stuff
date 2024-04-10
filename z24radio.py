import usys
import ustruct as struct
import utime
from machine import Pin, SPI, SoftSPI
from nrf24l01 import NRF24L01
from micropython import const

# Responder pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)
# Responder pauses an additional _RESPONER_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) initiator time to get into receive mode. The
# initiator may be a slow device. Value tested with Pyboard, ESP32 and ESP8266.
_RESPONDER_SEND_DELAY = const(10)


# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")


class ZRF24:
    
    def __init__(self, sck_n=10, mosi_n=11, miso_n=12, bus_n=1, cse_n=9, csn_n=13, payload_size=16):
        # payload_size is in bytes, not bits. max of 32.
        
        self.spi = SPI(bus_n, sck=Pin(sck_n), mosi=Pin(mosi_n), miso=Pin(miso_n))
        self.csn = Pin(self.csn_n, mode=Pin.OUT, value=1)
        self.cse = Pin(self.cse_n, mode=Pin.OUT, value=0)
        self.nrf = NRF24L01(self.spi, self.csn, self.cse, payload_size=payload_size)
        self.nrf.open_tx_pipe(pipes[0])
        self.nrf.open_rx_pipe(1, pipes[1])
    
    def listen(self):
        self.nrf.start_listening()
    
    def send(self, packed_message):
        self.nrf.stop_listening()
        self.nrf.send(packed_message)
    
    def receive(self, struct_format_str, recv_timeout=-1):
        if nrf.any():
          start = utime.ticks_ms()
            while nrf.any():                
                if utime.ticks_diff(utime.ticks_ms(), start) > recv_timeout:
                    return None
                buf = nrf.recv()
                return struct.unpack(struct_format_str, buf)
        
    
