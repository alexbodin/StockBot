
####################
#
#   Account
#   for StockBot
#   by Alexander Bodin
#
####################

import json
import sys

class Account:
    def __init__(self, name, localcurrency):
        self.name = name
        self.cash = 0
        self.localcurrency = localcurrency
        self.stocks = {}
        self.depositHistory = []
        self.deposits = 0
        self.withdrawals = 0
        
        try:
            account_file = open("data/" + name + ".json", "r", encoding="utf8")

            data = json.load(account_file)
            #print(data)
            self.fromJson(data)
            account_file.close()
        
        except FileNotFoundError:
            print("File not found")
            self.saveToFile()
        except:
            print("Generic error: ", sys.exc_info()[0])
        finally:
            account_file.close()

    def clearAccount(self):
        #account_file = open("Konto" + ".json", "w+", encoding="utf8")
        #account_file.write("")
        #account_file.close()
        self.cash = 0
        self.stocks = {}
        self.depositHistory = []
        self.deposits = 0
        self.withdrawals = 0
        self.saveToFile()

    def saveToFile(self):
        try:
            account_file = open("data/" + self.name + ".json", "w+", encoding="utf8")
            account_file.write(self.toJson())
        except:
            print("Error writing to accountfile")
        finally:
            account_file.close()

    def toJson(self):

        stocks = '{\n\t\t'
        for s in self.stocks:
            stocks += '"' + s + '":' + self.stocks[s].toJson() + ",\n\t\t"
        if len(self.stocks) > 0:
            stocks = stocks[:-4]
        stocks += '\n\t}\n'

        depositHistory = '[\n\t\t' 
        for i in range(len(self.depositHistory)):
            depositHistory += str(self.depositHistory[i]) + ',\n\t\t'
        if len(self.depositHistory) > 0:
            depositHistory = depositHistory[:-4]
        depositHistory += '\n\t]'

        jsonstr = (
            '{\n\t"name":"' + self.name +
            '",\n\t"cash":' + str(self.cash) +
            ',\n\t"localcurrency":"' + self.localcurrency +
            '",\n\t"deposits":' + str(self.deposits) +
            ',\n\t"withdrawals":' + str(self.withdrawals) +
            ',\n\t"depositHistory":' + depositHistory +
            ',\n\t"stocks":' + stocks + '}'
        )
        return jsonstr

    def fromJson(self, data):
        
            self.cash = data["cash"]
            self.localcurrency = data["localcurrency"]
            #self.stocks = data["stocks"]
            self.depositHistory = data["depositHistory"]
            self.deposits = data["deposits"]
            self.withdrawals = data["withdrawals"]

            for stock in data["stocks"]:
                dstock = data["stocks"][stock]
                self.stocks[stock] = Stock(dstock["name"], dstock["currency"])
                self.stocks[stock].history = dstock["history"]
                self.stocks[stock].amount = dstock["amount"]
                self.stocks[stock].averageprice = dstock["averageprice"]
                self.stocks[stock].averagepricelocal = dstock["averagepricelocal"]
                self.stocks[stock].totalcost = dstock["totalcost"]


    def deposit(self, amount, time):
        self.depositHistory.append([amount, time])
        self.deposits += amount
        self._addCash(amount)

    def withdraw(self, amount, time):
        if self._useCash(amount):
            self.depositHistory.append({-amount, time})
            self.withdrawals += amount

    def _addCash(self, amount):
        self.cash += amount

    def _useCash(self, amount):
        if self.getBalance() < amount:
            print("Warning: Cash balance is less than 0")
            print("Failed to use cash, balance too low!")
            return False
        else:
            self.cash -= amount
            return True

    def getBalance(self):
        return self.cash

    
    def buyStock(self, symbol, name, amount, currency, price, pricelocal, courtage, time):
        """ Adds a stock to account, price is for example in USD and price local is
        your local (accounts) currency eg SEK """
        
        if (self.getBalance() > (pricelocal * amount + courtage)):
            self._useCash(pricelocal * amount + courtage)
        else:
            print("Failed to buy stock, not enough funds (" + self.getBalance()
                + " of " + pricelocal * amount + courtage + ")")
            return False

        if symbol not in self.stocks:
            self.stocks[symbol] = Stock(name, currency)
        
        self.stocks[symbol].buy(amount, price, pricelocal, courtage, time)

        return True

    def sellStock(self, symbol, amount, price, pricelocal, courtage, time):
        if (self.stocks[symbol].getAmount() > amount):
            self.stocks[symbol].sell(amount, price, pricelocal, courtage, time)
            self._addCash(pricelocal*amount - courtage)
            return True
        else:
            print("Failed to sell " + amount + " stock, you only own "
                + self.stocks[symbol].getAmount())
            return False






class Stock:
    def __init__(self, name, currency):
        self.name = name
        self.history = []
        self.amount = 0
        self.currency = currency
        self.averageprice = 0
        self.averagepricelocal = 0
        self.totalcost = 0


    def buy(self, amount, price, pricelocal, courtage, time):
        self.history.append({
            "amount": amount,
            "price": price,
            "pricelocal": pricelocal,
            "exchangerate": (pricelocal / price),
            "courtage": courtage,
            "time": time
            })
        self.update()

    def sell(self, amount, price, pricelocal, courtage, time):
        self.buy(-amount, price, pricelocal, courtage, time)

    def update(self):

        amount = 0
        cost = 0
        costlocal = 0
        courtage = 0

        for i in range(len(self.history)):
            amount += self.history[i]["amount"]
            cost += self.history[i]["price"]*self.history[i]["amount"]
            costlocal += self.history[i]["pricelocal"]*self.history[i]["amount"]
            courtage += self.history[i]["courtage"]


        self.amount = amount
        self.averageprice = cost / amount
        self.averagepricelocal = costlocal / amount
        self.totalcost = costlocal + courtage

    def getAmount(self):
        return self.amount
    
    def getAveragePrice(self):
        return self.averageprice
    
    def getAveragePriceLocal(self):
        return self.averagepricelocal

    def getTotalCost(self):
        return self.totalcost

    def getHistory(self):
        return self.history

    def toJson(self):

        hist = '['

        for h in range(len(self.history)):
            hist += (
                '{\n\t\t\t\t\t"amount":' + str(self.history[h]["amount"]) +
                ',\n\t\t\t\t\t"price":' + str(self.history[h]["price"]) +
                ',\n\t\t\t\t\t"pricelocal":' + str(self.history[h]["pricelocal"]) +
                ',\n\t\t\t\t\t"exchangerate":' + str(self.history[h]["exchangerate"]) +
                ',\n\t\t\t\t\t"courtage":' + str(self.history[h]["courtage"]) +
                ',\n\t\t\t\t\t"time":' + str(self.history[h]["time"]) + '\n\t\t\t\t},\n\t\t\t\t'
                )
        if len(self.history) > 0:
            hist = hist[:-6]
        hist += '\n\t\t\t]'

        jsonstr = (
            '{\n\t\t\t"name":"' + self.name +
            '",\n\t\t\t"amount":' + str(self.amount) +
            ',\n\t\t\t"currency":"' + self.currency +
            '",\n\t\t\t"averageprice":' + str(self.averageprice) +
            ',\n\t\t\t"averagepricelocal":' + str(self.averagepricelocal) +
            ',\n\t\t\t"totalcost":' + str(self.totalcost) +
            ',\n\t\t\t"history":' + hist + '\n\t\t}'
            )

        return jsonstr


