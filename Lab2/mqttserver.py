print("Hello MQTT SERVER")
import paho.mqtt.client as mqttclient
import time
import json
import random
import serial.tools.list_ports


BROKER_ADDRESS = "mqttserver.tk"
PORT = 1883


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", client, userdata, message.payload.decode("utf-8"))
    
    
    # if len(bbc_port) > 0:
    #     ser.write((str(cmd) + "#").encode())
AIO_FEED_ID = ['/bkiot/1912526/led', '/bkiot/1912526/pump']
def connected(client, usedata, flags, rc):
    if rc == 0:
        print("SERVER  connected successfully!!")
        for feed in AIO_FEED_ID:
            client.subscribe(feed)
    else:
        print("Connection is failed")


client = mqttclient.Client()
client.username_pw_set("bkiot", '12345678')

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message



while True:

    # random temperature and humidity
    temp = random.randrange(0, 100)
    humi = random.randrange(0, 100)
    
    collect_data = {'temperature': temp, 'humidity': humi}
    print(collect_data)

    x = client.publish('/bkiot/1912526/status', json.dumps(collect_data), 1)
    print(x)
    time.sleep(3)


