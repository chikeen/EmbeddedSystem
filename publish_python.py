# import paho.mqtt.publish as publish
# publish.single("IC.embedded/Iceberg","WHAT IS UP!", hostname="test.mosquitto.org")
# print("Done")


# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("IC.embedded/Iceberg", "Hello", hostname="test.mosquitto.org")
publish.single("IC.embedded/Iceberg", "World!",
               hostname="test.mosquitto.org")
print("Done")
