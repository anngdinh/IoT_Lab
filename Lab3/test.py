print("Hi ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import random
import serial.tools.list_ports

mess = ""
bbc_port = "COM7"
if len(bbc_port) > 0:
    ser = serial.Serial(port=bbc_port, baudrate=115200)

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        collect_data = {"temp": int(splitData[2])}
        client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    if splitData[1] == "LIGHT":
        collect_data = {"light": int(splitData[2])}
        client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "y0wYWMhxmW5ePA4LEcEz"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    jsonobj = json.loads(message.payload)
    print("Received: ", jsonobj)
    temp_data = {}
    try:
        if jsonobj['method'] == "setLED":
            temp_data['BUTTON_LED'] = jsonobj['params']
            message = 'L' + str(jsonobj['params'])
            print(message)
            ser.write((str(message) + "#").encode())
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        elif jsonobj['method'] == "setPUMP":
            temp_data['BUTTON_PUMP'] = jsonobj['params']
            message = 'P' + str(jsonobj['params'])
            print(message)
            ser.write((str(message) + "#").encode())
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        # if jsonobj['method'] == "setLED":
        #     temp_data['valueLED'] = jsonobj['params']
        #     client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
        # elif jsonobj['method'] == "setPUMP":
        #     temp_data['valuePUMP'] = jsonobj['params']
        #     client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        print("except when try publish")
        pass
    
    # if len(bbc_port) > 0:
    #     ser.write((str(cmd) + "#").encode())

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


while True:

    readSerial()
    time.sleep(1)




# conda activate IOT