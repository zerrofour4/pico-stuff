import usys
import ustruct as struct
import utime
from machine import Pin, SPI
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


class ZRF24:
    '''
    spi = SPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12))
    cfg = {"spi": spi, "csn": 9, "ce": 13}
    '''
    
    def __init__(self, rx_pipe=None, tx_pipe=None, sck_n=10, mosi_n=11, miso_n=12, bus_n=1, csn_n=9, cse_n=13, payload_size=32):
        # payload_size is in bytes, not bits. max of 32.
        
        self.spi = SPI(bus_n, sck=Pin(sck_n), mosi=Pin(mosi_n), miso=Pin(miso_n))
        self.csn = Pin(csn_n, mode=Pin.OUT, value=1)
        self.cse = Pin(cse_n, mode=Pin.OUT, value=0)
        self.nrf = NRF24L01(self.spi, self.csn, self.cse, payload_size=payload_size)
        if tx_pipe:
            self.nrf.open_tx_pipe(tx_pipe)
        if rx_pipe:
            self.nrf.open_rx_pipe(1, rx_pipe)
        if (tx_pipe is None and rx_pipe is None):
            raise OSError("need a pipe")
    
    def start_listening(self):
        self.nrf.start_listening()
    
    def stop_listening(self):
        self.nrf.stop_listening()
    
    def send(self, packed_message):
        self.stop_listening()
        try:
            self.nrf.send(packed_message)
        except OSError:
            status = False
        status = True
        self.start_listening()
        return status
    
    def receive(self, struct_format_str, recv_timeout=500):
        if self.nrf.any():
          start = utime.ticks_ms()
          while self.nrf.any():                
            if utime.ticks_diff(utime.ticks_ms(), start) > recv_timeout:
              return None
            self.stop_listening()
            buf = self.nrf.recv()
            print(buf)
            utime.sleep_ms(_RX_POLL_DELAY)
            self.start_listening()
            return struct.unpack(struct_format_str, buf)
        
    
