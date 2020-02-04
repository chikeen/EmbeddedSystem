import smbus
import time
import paho.mqtt.client as mqtt
import datetime
import json
import ssl
bus = smbus.SMBus(1)
i2c_addr = 0x48  # our slave address

# below are the 4 different kind of register in ADC1115 module
status_reg = 0x00
mode_reg = 0x01
dataH_reg = 0x02
dataL_reg = 0x03
# this is to configure the device
bus.write_word_data(i2c_addr, mode_reg, 0x8384)

# this is to write to pointer register
bus.write_byte(i2c_addr, 0)

# this is to continuously read the conversion register
# (RMB ADC1115 is a ADC module: so the reading here is the voltage)


client = mqtt.Client()

client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",
               keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)

client.connect("test.mosquitto.org", port=8884)


while(True):
    val_swapped = bus.read_word_data(i2c_addr, 0x00)
    val = (val_swapped & 0xFF) << 8 | (val_swapped >> 8)
    val = int((abs(val - 0) /1) * 1)
    time_now = datetime.datetime.utcnow().__str__()
    my_dict = {"value": val, "time": time_now}
    packet_json = json.dumps(my_dict)
    client.publish("IC.embedded/Faraday", packet_json)

    time.sleep(1)

print("Done")
