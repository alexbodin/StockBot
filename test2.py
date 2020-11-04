
import datetime as dt

t = 1601904900

a = str(dt.datetime.utcfromtimestamp(t).strftime("%Y/%m/%d %H:%M:%S"))


print(a)