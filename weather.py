import sys
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import pickledb

arguments =  str(sys.argv)
location = sys.argv[1][3:]
api_key = '7d1f103da154c35b3e1c921ad8d09113'
db = pickledb.load('history.db', False)


if '-h' not in arguments and '-f' not in arguments :
    print('current weather info')
    serviceurl = 'http://api.openweathermap.org/data/2.5/weather?'
    url = serviceurl + 'q=' + location + '&APPID=' + api_key
    print('Retrieveing', url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    try:
        js = json.loads(data)
    except:
        js = None
    print(js)
    temp = js['main']['temp']
    hum = js['main']['humidity']
    time_stamp = js['dt']


    dict_key = location
    dict_data = [temp, hum]
    print('At', location, 'and time', time_stamp , 'the temperature is:', temp, 'while the humidity is', hum)
    dict = {str(time_stamp):dict_data}
    print(dict)

    if location not in db.getall():
        db.set(dict_key, dict)
        db.dump()
    else:
        db.dadd(location,(str(time_stamp),dict_data))
        db.dump()

elif'-f' in arguments :
    print ('forecast data')
    serviceurl = 'http://api.openweathermap.org/data/2.5/weather?'
    url = serviceurl + 'q=' + location + '&APPID=' + api_key
    print(url)
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    try:
        js = json.loads(data)
    except:
        js = None

    lon = js['coord']['lon']
    lon = str(lon)
    lat = js['coord']['lat']
    lat = str(lat)

    serviceurl1 = 'https://api.openweathermap.org/data/2.5/onecall?'
    url1 = serviceurl1 + 'lat=' + lat + '&lon=' + lon + '&appid=' + api_key
    print('Retrieving', url1)
    uh1 = urllib.request.urlopen(url1)
    data1 = uh1.read().decode()
    try:
        js1 = json.loads(data1)
    except:
        js1 = None

    print(js1['hourly'])
    start_time = js1['current']['dt']
    x = list(range(24))

    for a in x:
        time = js1['hourly'][a]['dt']
        temp = js1['hourly'][a]['temp']
        hum = js1['hourly'][a]['humidity']
        print('At time:', time, ', temperature is:', temp, 'and humidity is:',hum)


else:
    log = db.dgetall(location)
    print('A history of weather data obtained from', location)
    for key in log:
        print('At time', key, 'the temperature and humidity are', log[key])
