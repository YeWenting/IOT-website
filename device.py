# Submit Post Data
import urllib, urllib2, json, random
import threading
from time import sleep


url = r'http://127.0.0.1:8000/api/addlog/'


def start_device(SN, max_temp, min_temp, interval):
    working = True
    while True:
        # If the device is working
        if working:
            temp = random.randint(max_temp, min_temp)
            data = urllib.urlencode([('SN', SN), ('temperature', temp)])
            req = urllib2.Request(url)
            fd = urllib2.urlopen(req, data)

            # Read the json response
            resp = json.load(fd)
            print(SN + " is working.  add: " + str(resp['add']) + " work: " + str(resp['is_open']) + "\n")
            if not resp['is_open']:
                working = False
            else:
                sleep(interval)

        # If the device has been shut down
        else:
            data = urllib.urlencode([('SN', SN)])
            req = urllib2.Request(url)
            fd = urllib2.urlopen(req, data)

            # Read the json response
            resp = json.load(fd)
            print(SN + " isn't working.  work: " + str(resp['is_open']) + "\n")
            if resp['is_open']:
                working = True
            else:
                sleep(interval)

# Read the file
f = open('config.txt', 'r')
data = f.read()
rows = data.split("\n")
SN = []
min_temp = []
max_temp = []
for row in rows:
    temp = row.split(' ')
    SN.append(str(temp[0]))
    min_temp.append(int(temp[1]))
    max_temp.append(int(temp[2]))


# Run the device
threads = []
for i in range(len(SN)):
    print(SN[i])
    t = threading.Thread(target=start_device, args=(SN[i], min_temp[i], max_temp[i], 10))
    threads.append(t)

for t in threads:
    t.setDaemon(True)
    t.start()

t.join()
