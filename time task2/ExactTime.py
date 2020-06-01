import requests
import time
import re


url = "https://www.timeserver.ru/"
time_url = requests.get(url)
rep = int(re.search(r'utcTime: ?([^,>]+)', time_url.content.decode('utf-8')).group(1)[:-3])

with open('sabotage.txt', "r") as f:
    plus_time = int(f.read())

result = time.gmtime(rep+plus_time)

print('UTC time', result.tm_hour, result.tm_min, result.tm_sec, sep=':')