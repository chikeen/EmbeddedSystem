import paho.mqtt.client as mqtt
import time
import json
import datetime
import ssl


def connect_me(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("IC.embedded/Faraday")


def message_me(client, userdata, msg):
    my_json = json.loads(msg.payload)
    print(my_json)


client = mqtt.Client()
client.on_connect = connect_me
client.on_message = message_me

client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",
               keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)

client.connect("test.mosquitto.org", 8884, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions

client.loop_forever()


# client.loop_start()
# time.sleep(8)
# client.loop_stop()
# print("DONE!!!")
