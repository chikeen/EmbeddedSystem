import smbus
import time
import paho.mqtt.client as mqtt
import datetime
import json
# import ssl
import math

#setting up sensor and smBUS
bus = smbus.SMBus(1)
i2c_addr_flex = 0x48 # our flex sensor slave address
i2c_addr_compass = 0x0c # our compass sensor slave address

def read_flex (i2c_addr, duration, readings_per_median=3):
    #below are the 4 different kind of register in ADC1115 module
    status_reg = 0x00
    mode_reg = 0x01
    dataH_reg = 0x02
    dataL_reg = 0x03
    
    #this is to configure the device
    bus.write_word_data(i2c_addr, mode_reg, 0x8384)

    #this is to write to pointer register
    bus.write_byte(i2c_addr, 0)

    val_list = []

    for i in range(readings_per_median):
        
        val_swapped = bus.read_word_data(i2c_addr, 0x00)
        val = (val_swapped & 0xFF) <<8 | (val_swapped >>8)
        val = int((abs(val - 9000) /7500) * 2100) #scaling sensor data
        #print ("flex reading: ", val)
        time.sleep(duration/readings_per_median)
        print("flex reading: ", val)
        val_list.append(val)
    val_list.sort()
    print ("median reading: ", val_list[math.floor(len(val_list)/2)])
    return val_list[math.floor(len(val_list)/2)]
        

        
def read_compass(i2c_addr, duration, readings_per_median=1):
    #!!! KEEP READINGS PER MEDIAN TO 1 until you have support for angular wrap around (like robotics).

    for i in range(readings_per_median):

        # Select write register command, 0x60(96)
        # AH = 0x00, AL = 0x5C, GAIN_SEL = 5, Address register (0x00 << 2)
        config = [0x00, 0x5C, 0x00]
        bus.write_i2c_block_data(i2c_addr, 0x60, config)

        # Read data back, 1 byte, (ACK byte)
        # Status byte
        data = bus.read_byte(i2c_addr)

        # AH = 0x02, AL = 0xB4, RES for magnetic measurement = 0, Address register (0x02 << 2)
        config = [0x02, 0xB4, 0x08]
        bus.write_i2c_block_data(i2c_addr, 0x60, config)

        # Read data back, 1 bytem (ACK byte)
        # Status byte
        data = bus.read_byte(i2c_addr)

        # Start single meaurement mode, X, Y, Z-Axis enabled
        bus.write_byte(i2c_addr, 0x3E)

        # Read data back, 1 byte
        # Status byte
        data = bus.read_byte(0x0C)

        time.sleep(0.5)

        # Read data back from 0x4E(78), 7 bytes
        # Status, xMag msb, xMag lsb, yMag msb, yMag lsb, zMag msb, zMag lsb
        data = bus.read_i2c_block_data(i2c_addr, 0x4E, 7)


        xMag = data[1] * 256 + data[2]
        if xMag > 32767 :
            xMag -= 65536

        yMag = data[3] * 256 + data[4]
        if yMag > 32767 :
            yMag -= 65536

        zMag = data[5] * 256 + data[6]
        if zMag > 32767 :
            zMag -= 65536
            
        #heading = math.atan2(yMag, xMag) * 180 / math.pi
        
        # Debug
#         print(data)
#         print("Magnetice Field (x, y, z) = ", xMag, yMag, zMag)
#         print(heading + 330)

        time.sleep(duration/ readings_per_median)
        #no_of_reading = no_of_reading - 1
    print("xMag: ",xMag)
    print("yMag: ",yMag)
    print("zMag: ",zMag)
    return (xMag, yMag, zMag)
 

# Setting mqtt connection
client = mqtt.Client()
# client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",
#                keyfile="client.key", tls_version=ssl.PROTOCOL_TLSv1_2)

client.connect("test.mosquitto.org", port=1883)
client.publish("IC.embedded/Faraday", "HELLO")


mode = "Home" # or Music, Sports, Sleep


while(True):

    flex_val = read_flex(i2c_addr_flex, 0.5, 3) # reading 1 times in 1 sec
    compass_val = read_compass(i2c_addr_compass, 0.4, 1) # reading 1 times in 1 sec
    
    
    if((compass_val[2] > 63 or compass_val[2] < 40) and mode is not "Sleep"):
        print("Mode: ", mode, "-> Sleep, compass_val= ", compass_val)
        mode = "Sleep"
    
    if((compass_val[2] <= 63 and compass_val[2] >= 40) and mode is "Sleep"):
        print("Mode: ", mode, "-> Home, compass_val= ", compass_val)
        mode = "Home"
        
        
    # packaging json payload
    time_now = datetime.datetime.utcnow().__str__()
    my_dict = {"mode": mode, "value": flex_val, "time": time_now}
    packet_json = json.dumps(my_dict)
    
    client.publish("IC.embedded/Faraday", packet_json)

    #time.sleep(1)

print("Done")

