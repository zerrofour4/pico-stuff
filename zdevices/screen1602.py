from machine import I2C, Pin
from lib.lcd1602 import LCD
import time

class Screen:
    def __init__(self, sda, sdc):
        i2c = I2C(0, sda=Pin(sda), scl=Pin(sdc), freq=400000)
        self.lcd = LCD(i2c)
        
        self.pages = list()
        self.lcd.clear()
    
    def display_page(self, page_num):
        self.lcd.clear()
        try:
            self.lcd.message(self.pages[page_num])
        except IndexError:
            self.lcd.message("Invalid page " + str(page_num))
    
    def add_page(self, contents):
        lines = contents.split('\n')
        if len(lines) > 2:
            print("pages can only have 2 newline characters")
            return
        for line in lines:
            print(line)
            if len(line) > 16:
                print("line too long: " + line )
                return
        self.pages.append(contents)
        
    def cycle_pages(self, delay_seconds):
        if len(self.pages) == 0:
            print("no pages")
            return
        for page in self.pages:
            self.lcd.clear()
            self.lcd.message(page)
            time.sleep(delay_seconds)
        
