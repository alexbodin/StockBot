
#import matplotlib.pyplot as plt
import json
import plotly.graph_objects as go
import datetime as dt

datafile = open("data/" + "TSLAcandles.json", "r", encoding="utf8")
data = json.load(datafile)
datafile.close()

#x = []
#for i in range(len(data["c"])):
#    x.append(i)

#plt.plot(x,data["c"])
#plt.show()

time = []
for t in range(len(data['t'])):
    aaa = dt.datetime.utcfromtimestamp(data['t'][t]).strftime("%Y/%m/%d %H:%M")
    time.append(aaa)
print(time)

fig = go.Figure(data=[go.Candlestick(x=time,
                open=data['o'],
                high=data['h'],
                low=data['l'],
                close=data['c'])])

fig.show()


#https://plotly.com/python/candlestick-charts/