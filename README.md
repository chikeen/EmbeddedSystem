# Bamboo

## Quick Links

1. Github repo for the Bamboo cross-platform app: https://github.com/zenasgram/Bamboo
2. Official Website:


## Introduction

...


## Technical Details:

### Hardware 

![Circuit Diagram of Bamboo](Hardware_circuit.png)

In Bamboo, the main sensor is a Flex sensor where its resistance increases as the sensor's curvature increases. This enable us to measure the curvature of user's neck/upper back and inform the user if the user is slouching too much. Since the flex sensor is analog, an additional op-amp (TL072CP) and an ADC (ADS1115) are used alongside the flex sensor to enable complete i2c communication with Pi Zero. 

Besides the main sensor, a additional 3D magnetometer (MLX 90393) is used to tell if the user is currently lying down or standing/sitting upright. This provides further information to the application, enabling feature such as auto-switching between modes. 

These two slave sensor are then connected to the master Pi Zero via i2c communication. Pi Zero will handle the next step of preprocessing of raw sensor data and communication with application via Mqtt broker. 

### Connection (Mqtt broker)
... TODO: chris

### Application
... TODO: zenas


## Credits:

Zenas (https://github.com/zenasgram), Chris (https://github.com/ChrisDeverall), CK (https://github.com/chikeen) at Imperial College London 2020
