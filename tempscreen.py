from zdevices.screen1602 import Screen
from zdevices.dht11 import ZDHT11
import time
import network
import socket
import secrets
import _thread



# screen
SDA = 20
SDC = 21

# dht11

def temp_humidity_display():
    lcd = Screen(SDA, SDC)
    dht11 = ZDHT11(15, "f")
    


    lcd.lcd.clear()
    temp, humidity = dht11.measure()
    msg = f"Temp: {temp}\nHumidity: {humidity}"
    lcd.lcd.message(msg)
    time.sleep(1.1)
    
    while True:
        temp, humidity = dht11.measure()
        if temp == 69 :
            lcd.lcd.write(6, 0, str(temp) + " (Nice)")
        else:
            lcd.lcd.write(6, 0, str(temp))
            for i in range(8, 15):
                lcd.lcd.write(i, 0, " ")
                
        lcd.lcd.write(10, 1, str(humidity))
        time.sleep(1.1)


def web_server():

    # Select the onboard LED
    led = machine.Pin("LED", machine.Pin.OUT)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    stateis = "LED is OFF"

    html = """<!DOCTYPE html>
    <html>
       <head>
         <title>Web Server On Pico W </title>
       </head>
      <body>
          <h1>Pico Wireless Web Server</h1>
          <p>%s</p>
          <a href="/light/on">Turn On</a>
          <a href="/light/off">Turn Off</a>
      </body>
    </html>
    """

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
      raise RuntimeError('network connection failed')
    else:
      print('We are connected to WiFI access point:', secrets.SSID)
      status = wlan.ifconfig()
      print( 'The IP address of the pico W is:', status[0] )

    # Open socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    print('addr:', addr)
    s = socket.socket()
    #if not addr:
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

# Listen for connections
    while True:
      try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        request = str(request)
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        if led_on == 6:
          print("led on")
          led.value(1)
          stateis = "LED is ON"

        if led_off == 6:
          print("led off")
          led.value(0)
          stateis = "LED is OFF"
        # generate the we page with the stateis as a parameter
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

      except OSError as e:
        cl.close()
        print('connection closed')


if __name__ == "__main__":
    #_thread.start_new_thread(temp_humidity_display,())
    #web_server()
    temp_humidity_display()