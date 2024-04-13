from zdevices import z24radio
from zdevices import button
import struct
import utime



if __name__ == "__main__":
    # pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
    tx_pipe = b"\xe1\xf0\xf0\xf0\xf0"
    rx_pipe = b"\xd2\xf0\xf0\xf0\xf0"
    red = button.Button(16,"red")
    yellow = button.Button(17,"yellow")
    
    buttons = [red, yellow]
    
    radio = z24radio.ZRF24(tx_pipe=tx_pipe, payload_size=4)
    radio.stop_listening()
    num_leds = 0
    while True:
        press = False
        if red.read():
            press = True
            print("pressed " + red.label)
            num_leds += 1
            if num_leds > 8:
                num_leds = 8
        if yellow.read():
            press = True
            num_leds -= 1
            if num_leds < 0:
                num_leds = 0
        
        if press:
            d = struct.pack("i", num_leds)
            print(d)
            status = radio.send(d)
            print("received: " + str(status))
            utime.sleep(.080)


