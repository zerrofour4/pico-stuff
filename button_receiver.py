from zdevices import z24radio
from zdevices import shift_register

if __name__ == "__main__":
    rx_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    tx_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    
    radio = z24radio.ZRF24(rx_pipe, tx_pipe)
    reg = shift_register.ShiftRegister(0, 1, 2)
    reg.write(0)
    radio.start_listening()
    data_format = "i"
    num_leds = 0
    while True:
        rd = radio.receive(data_format)
        if rd is not None:
          num_leds = rd[0]
          print(num_leds)
          reg.fill(num_leds)
