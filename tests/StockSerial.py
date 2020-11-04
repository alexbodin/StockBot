import serial
import time
import requests

sym = "AAPL"

arduino = serial.Serial('COM3', 9600, timeout=5)
time.sleep(5)

while True:
    r = requests.get('https://finnhub.io/api/v1/quote?symbol=' + sym + '&token=bqs4fifrh5r92r4us2k0')
    print(r.json())

    out = sym + ',' + str(r.json()['c']) + ',' + str(r.json()['pc']) + '\n'

    arduino.write(out.encode("ASCII"))
    print("Write: " + out)

    time.sleep(1.5)

arduino.close()