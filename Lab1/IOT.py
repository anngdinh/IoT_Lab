print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import random
import geocoder

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "h6SgC5NTVj1WBonOYE0F"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client(" Gateway _Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intesity = 100
counter = 0

# longitude = 10.8231
# latitude = 106.6297

longitude = 106.7
latitude = 10.6

while True:
    # get current position by geocoder
    g = geocoder.ip('me')
    # print(g.latlng)
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    
    # random temperature and humidity
    temp = random.randrange(200, 300)
    humi = random.randrange(0, 100)
    
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intesity, "longitude": longitude, "latitude":latitude}
    print(collect_data)
    light_intesity += 1

    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(5)



# # importing geopy library
# from geopy.geocoders import Nominatim
 
# # calling the Nominatim tool
# loc = Nominatim(user_agent="GetLoc")
 
# # entering the location name
# getLoc = loc.geocode("Gosainganj Lucknow")
 
# # printing address
# print(getLoc.address)
 
# # printing latitude and longitude
# print("Latitude = ", getLoc.latitude, "\n")
# print("Longitude = ", getLoc.longitude)