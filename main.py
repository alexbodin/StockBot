
####################
#
#   StockBot
#   A stock analysing bot
#   by Alexander Bodin
#
####################


import web_api
#import ui
from account import Account
#from time import sleep
import time
import datetime


def accountStuff():

    konto = Account("Konto", "SEK")
    konto.clearAccount()

    #konto.deposit(100000,0)
    #konto.deposit(100000,0)
    #konto.buyStock("TSLA", "Tesla", 10, "USD", 420, 420*9.11, 14, 0)
    #konto.buyStock("TSLA", "Tesla", 10, "USD", 390, 390*8.56, 14, 0)
    #konto.buyStock("TSLA", "Tesla", 10, "USD", 450, 450*8.87, 14, 0)
    #konto.sellStock("TSLA", 10, 500, 500*9.1, 14, 0)
    #print(konto.getBalance())
    #print(konto.stocks["TSLA"].getAmount())
    #print(konto.stocks["TSLA"].getAveragePrice())
    #print(konto.stocks["TSLA"].getAveragePriceLocal())
    #print(konto.stocks["TSLA"].getTotalCost())
    #print(konto.stocks["TSLA"].getHistory())

    #print(konto.toJson())
    #konto.saveToFile()

    #TODO: import transactions from Avanza



if __name__ == "__main__":
    #StockStream("TSLA")

    #pc = web_api.getPreviousClose("TSLA")
    #wsa = web_api.openStream(["TSLA"])
    #wsa = web_api.openStream(["BINANCE:BTCUSDT"])

    now = int(time.time())
    web_api.getCandles('TSLA', 1, now - 3*24*60*60, now)
    web_api.getCandles('AAPL', 1, now - 3*24*60*60, now)
    web_api.getCandles('AMZN', 1, now - 3*24*60*60, now)
    #ui.graph_data('TSLA')
    #accountStuff()

    #s = "01/09/2020"
    #e = "26/09/2020"
    #start = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
    #end = int(time.mktime(datetime.datetime.strptime(e, "%d/%m/%Y").timetuple()))

    #while True:
    #    pass