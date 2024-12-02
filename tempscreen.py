from machine import Pin,SPI
from zdevices.dht11 import ZDHT11
from zdevices.keypad import Keypad4x4

import framebuf
import time

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


dht11 = ZDHT11(18, "f")


class OLED_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 64
        
        self.rotate = 180 #only 0 and 180 
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,2000_000)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()
        
        self.white =   0xffff
        self.balck =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        
        self.write_cmd(0xAE)#turn off OLED display

        self.write_cmd(0x00)   #set lower column address
        self.write_cmd(0x10)   #set higher column address 

        self.write_cmd(0xB0)   #set page address 
      
        self.write_cmd(0xdc)    #et display start line 
        self.write_cmd(0x00) 
        self.write_cmd(0x81)    #contract control 
        self.write_cmd(0x6f)    #128
        self.write_cmd(0x21)    # Set Memory addressing mode (0x20/0x21) #
        if self.rotate == 0:
            self.write_cmd(0xa0)    #set segment remap
        elif self.rotate == 180:
            self.write_cmd(0xa1)
        self.write_cmd(0xc0)    #Com scan direction
        self.write_cmd(0xa4)   #Disable Entire Display On (0xA4/0xA5) 

        self.write_cmd(0xa6)    #normal / reverse
        self.write_cmd(0xa8)    #multiplex ratio 
        self.write_cmd(0x3f)    #duty = 1/64
  
        self.write_cmd(0xd3)    #set display offset 
        self.write_cmd(0x60)

        self.write_cmd(0xd5)    #set osc division 
        self.write_cmd(0x41)
    
        self.write_cmd(0xd9)    #set pre-charge period
        self.write_cmd(0x22)   

        self.write_cmd(0xdb)    #set vcomh 
        self.write_cmd(0x35)  
    
        self.write_cmd(0xad)    #set charge pump enable 
        self.write_cmd(0x8a)    #Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0XAF)
    def show(self):
        self.write_cmd(0xb0)
        for page in range(0,64):
            if self.rotate == 0:
                self.column =  63 - page    #set segment remap
            elif self.rotate == 180:
                self.column =  page
                          
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0,16):
                self.write_data(self.buffer[page*16+num])
        
class TextLine():
    
    def __init__(self, text, init_x, init_y):
        if len (text) > 16:
            raise Exception("line too long. 16 chars or less")
        self.text = text
        self.init_x = init_x
        self.init_y = init_y
        self.current_x = init_x
        self.current_y = init_y
        self.previous_x = init_x
        self.previous_y = init_y
        self.length = len(text)
        
        self.right_edge = init_x + (8 * len(text))
        
    def scroll_down(self, lines):
        self.previous_y = self.current_y
        self.current_y = self.current_y + (8 * lines)
        if self.current_y > 64:
            self.current_y = (self.current_y - 64)
    
    def scroll_up(self,lines):
        self.previous_y = self.current_y
        self.current_y = self.current_y - (8 * lines)
        if self.current_y > 64:
            self.current_y = (self.current_y - 64)
    
    def scroll_right(self, positions):
        self.previous_x = self.current_x
        self.current_x = self.current_x + (8 * positions)
        if self.current_x > 128:
            self.current_x = (self.current_x - 128)
        

    def right_blank(self):
        x = self.right_edge
        y = self.current_y
        w = 8 * (16 - self.length)
        h = 8
        return (x, y, w , h, OLED.balck, True)
    
    def temporary_append(self, word):
        if (len(word) + self.length) > 16:
            raise Exception("word is too long")
        return (word, self.right_edge + 8, self.current_y)

    def append(self, word):
        self.text = f"{self.text}{word}"
        if (len(word) + self.length) > 16:
            self.text = self.text[0:15]
        self.length = len(self.text)
    
    def blank_previous_line(self):
        x = 0
        y = self.previous_y
        w = 128
        h = 8
        return (x, y, w, h, OLED.balck, True)
    
    def blank_line(self):
        self.current_x = 0
        self.right_edge = 0
        self.text = ""
        self.length = 0
        return self.right_blank()
    
    def buf_text(self):
        return (self.text, self.current_x, self.current_y)
    
        


        
if __name__=='__main__':
    row_pins = [16,17,18,19]
    col_pins = [20, 21, 22, 26]
    k = Keypad4x4(row_pins, col_pins)
    
    
    OLED = OLED_1inch3()
    OLED.fill(0x0000) 

    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    OLED.show()
    first_line = TextLine("stuff", 0, 0)
    lines = []
    for i in range(8):
        lines.append(TextLine("", 0, 0 + (i * 8)))
    last_key = None
    line_index = 0
    blank_next = False
    while True:
        if keyA.value() == 0:
            for line in lines:
                OLED.rect(*line.blank_line())
                OLED.text(*line.buf_text())
            OLED.show()
            continue
        current_key = k.readKey()
        if current_key == last_key:
            continue
        if lines[line_index].length == 16 and line_index == 7:
            line_index = 0
            OLED.rect(*lines[0].blank_line())
        elif line_index < 7 and lines[line_index + 1].length == 16:
            blank_next = True
        elif lines[line_index].length == 16:
            line_index += 1
        if blank_next == True and lines[line_index].length == 16:
            OLED.rect(*lines[line_index + 1].blank_line())
            blank_next = False
        lines[line_index].append("".join(current_key))
        for line in lines:
            OLED.rect(*line.right_blank())
            OLED.text(*line.buf_text())

        OLED.show()
        time.sleep(.05)

        
        



