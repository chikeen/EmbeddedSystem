import smbus
import time
import paho.mqtt.client as mqtt

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


client.connect("test.mosquitto.org", port=1883)


while(True):
    val_swapped = bus.read_word_data(i2c_addr, 0x00)
    val = (val_swapped & 0xFF) << 8 | (val_swapped >> 8)
    client.publish("IC.embedded/Faraday", val)
    time.sleep(1)

print("Done")
