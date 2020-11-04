
####################
#
#   Web api interface
#   for StockBot
#   by Alexander Bodin
#
####################

import time
import json
import requests
import websocket
import threading
import _thread
import datetime as dt

token = "bto8i3748v6vfu050se0"
symbols = []
liveData = {}
candleSize = 5*60000 #milliseconds per candle


##### One time quotes #####


def _getData(symbol):
    req = requests.get('https://finnhub.io/api/v1/quote?' +
        'symbol=' + symbol +
        '&token=' + token)
    return req.json()


def getPreviousClose(symbol):
    data = _getData(symbol)
    now = time.localtime()
    if (now.tm_hour < 15 or (now.tm_hour == 15 and now.tm_min < 30)):
        return data['c']
    else:
        return data['pc']


def getCandles(symbol, resolution, starttime, endtime):
    """ Get historical data of a stock\n
        symbol: stock to get data from\n
        resolution: 1, 5, 15, 30, 60, D, W, M\n
        starttime: start time of data (UNIX time)\n
        endtime: end time of data (UNIX time) """
    
    req = requests.get("https://finnhub.io/api/v1/stock/candle?" +
        "symbol=" + symbol +
        "&resolution=" + str(resolution) +
        "&from=" + str(starttime) +
        "&to=" + str(endtime) +
        "&token=" + token)

    #print("https://finnhub.io/api/v1/stock/candle?" +
    #    "symbol=" + symbol +
    #    "&resolution=" + str(resolution) +
    #    "&from=" + str(starttime) +
    #    "&to=" + str(endtime) +
    #    "&token=" + token)
        
    print("Getting candle data for " + symbol +
        " at resolution " + str(resolution) +
        " from " + str(starttime) +
        " to " + str(endtime))

    saveDataToFile(symbol, req.json())


def saveDataToFile(filename, data):
    """ Saves data to csv file """

    #try:
    datafile = open("data/" + filename.replace(':', '_') + ".csv", "w+", encoding="utf8")
    datafile.write("Date,Open,High,Low,Close,Volume\n")
    for i in range(len(data['c'])):
        datafile.write(
            str(dt.datetime.fromtimestamp(data['t'][i]).strftime("%Y/%m/%d %H:%M:%S")) + "," +
            str(data['o'][i]) + "," +
            str(data['h'][i]) + "," +
            str(data['l'][i]) + "," +
            str(data['c'][i]) + "," +
            str(data['v'][i]) + "\n"
        )
    #except:
    #    print("Error writing to file")
    #finally:
    #    datafile.close()
    
#    try:
 #       datafile = open("data/" + filename.replace(':', '_') + ".json", "w+", encoding="utf8")
  #      datafile.write(data)
   # except:
    #    print("Error writing to file")
#    finally:
 #       datafile.close()

def appendDataToFile(filename, data):
    """ Appends json text to end of file """
    
    try:
        datafile = open("data/" + filename.replace(':', '_') + ".csv", "a", encoding="utf8")
        datafile.write(
            str(dt.datetime.fromtimestamp(data['t']).strftime("%Y/%m/%d %H:%M:%S")) + "," +
            str(data['o']) + "," +
            str(data['h']) + "," +
            str(data['l']) + "," +
            str(data['c']) + "," +
            str(data['v']) + "\n"
        )
    except:
        print("Error writing to file")
    finally:
        datafile.close()
#    try:
 #       datafile = open("data/" + filename.replace(':', '_') + ".json", "a", encoding="utf8")
  #      datafile.write(data)
   # except:
    #    print("Error appending to file")
#    finally:
 #       datafile.close()




##### Stream quotes #####

def openStream(stocks):
    """ Opens a stream of stock quotes which are saved in a variable quotes\n
        stocks: list of symbols eg ["TSLA", "AAPL"] """
    global symbols
    symbols = stocks
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + token,
                                on_message = _on_message,
                                on_error = _on_error,
                                on_close = _on_close)
    ws.on_open = _on_open
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    #ws.run_forever()
    return wst



def _on_message(ws, message):
    #print(message)
    try:
        r = json.loads(message)['data']
        #print(r)

        stock = liveData[r[0]['s'].replace(':', '_')]

        if (stock['t'] + candleSize < r[0]['t']):
            #save old candle
            if (stock['t'] != 0):
                appendDataToFile(r[0]['s'], stock)

            print("Begin new candle at: " + str(r[0]['t']))
            #begin new candle
            stock['c'] = r[0]['p']
            stock['h'] = r[0]['p']
            stock['l'] = r[0]['p']
            stock['o'] = r[0]['p']
            stock['t'] = r[0]['t']
            stock['v'] = r[0]['v']

        else:
            #update candle
            stock['c'] = r[0]['p']      # "close" is last price
            if (stock['h'] < r[0]['p']):
                stock['h'] = r[0]['p']  # if highest price
            if (stock['l'] > r[0]['p']):
                stock['l'] = r[0]['p']  # if lowest price
            stock['v'] += r[0]['v']     # add all volume
        
        #print(str(liveData))

        

    except:
        pass


def _on_error(ws, error):
    print(error)

def _on_close(ws):
    print("### closed ###")
    _thread.interrupt_main()
    

def _on_open(ws):
    
    now = int(time.time())

    for symbol in symbols:
        ws.send('{"type":"subscribe","symbol":"' + symbol + '"}')

        liveData[symbol.replace(':', '_')] = {
            'c': 0,
            'h': 0,
            'l': 0,
            'o': 0,
            't': 0,
            'v': 0
            }
        
        getCandles(symbol, 5, now - 7*24*60*60, now)

