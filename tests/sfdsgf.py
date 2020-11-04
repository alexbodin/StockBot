import time
now = time.localtime()
print(now.tm_hour < 15 or (now.tm_hour == 15 and now.tm_min < 30))