# import paho.mqtt.publish as publish
# publish.single("IC.embedded/Iceberg","WHAT IS UP!", hostname="test.mosquitto.org")
# print("Done")


# MQTT Publish Demo
# Publish two messages, to two different topics

#import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl


# def log_me(client, userdata, level, buf):
#    print("log: ", buf)


client = mqtt.Client()
#client.on_log = log_me
client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",
               keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)


client.connect("test.mosquitto.org", port=8884)
client.publish("IC.embedded/Iceberg", "Hey hows it going?")

#import ssl


# publish.single("IC.embedded/Iceberg", "Hello",
#                hostname="test.mosquitto.org", port=1883)
# publish.single("IC.embedded/Iceberg", "World!",
#                hostname="test.mosquitto.org", port=1883)
print("Done")
