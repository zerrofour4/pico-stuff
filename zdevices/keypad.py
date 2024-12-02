import machine
import time

class Keypad4x4:
    def __init__(self,row_pins, col_pins):
        self.characters = [["1","2","3","A"],["4","5","6","B"],["7","8","9","C"],["*","0","#","D"]]
        self.row = []
        self.col = []
        self.row_pins = row_pins
        self.col_pins = col_pins
        
        self._init_pins()
    
    def _init_pins(self):
        for i in range(4):
            self.row.append(None)
            self.row[i] = machine.Pin(self.row_pins[i], machine.Pin.OUT)
        for i in range(4):
            self.col.append(None)
            self.col[i] = machine.Pin(self.col_pins[i], machine.Pin.IN)
        
    def readKey(self):
        key = []
        for i in range(4):
            self.row[i].high()
            for j in range(4):
                if(self.col[j].value() == 1):
                    key.append(self.characters[i][j])
            self.row[i].low()
        if key == []:
            return None
        return key


if __name__ == "__main__":
    row_pins = [16,17,18,19]
    col_pins = [20, 21, 22, 26]


    k = Keypad4x4(row_pins, col_pins)


    last_key = None
    while True:
        current_key = k.readKey()
        if current_key == last_key:
            continue
        last_key = current_key
        if current_key != None:
            print(current_key)
        time.sleep(0.1)
        
