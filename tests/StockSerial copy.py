import serial
import time
import json
import requests
import websocket

arduino = serial.Serial('COM3', 9600, timeout=5)
#time.sleep(2)

sym = "TSLA"

#out = sym + ',1,1\n'
#arduino.write(out.encode("ASCII"))

req = requests.get('https://finnhub.io/api/v1/quote?symbol=' + sym + '&token=bqs4fifrh5r92r4us2k0')

now = time.localtime()
if (now.tm_hour < 15 or (now.tm_hour == 15 and now.tm_min < 30)):
    prevClose = req.json()['c']
else:
    prevClose = req.json()['pc']


def on_message(ws, message):
    #print(message)
    try:
        r = json.loads(message)['data'][0]
        #print(type(r))
        #print(r)
        out = 'u,' + str(r['p']) + ',' + str(prevClose) + '\n'

        arduino.write(out.encode("ASCII"))
        print("Write: " + out)
    except:
        pass


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")
    arduino.close()

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"' + sym + '"}')

if __name__ == "__main__":

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=bqs4fifrh5r92r4us2k0",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()