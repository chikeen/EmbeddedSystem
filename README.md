# Bamboo

## Quick Links

1. Github repo for the Bamboo cross-platform app: https://github.com/zenasgram/Bamboo
2. Official Website: https://koi-sprout-xmz8.squarespace.com/


## Introduction

Simply download the app and place the adhesive posture sensor on your back. Using our app, you’ll be able to visualise how your posture has progressed throughout the day. You’ll also receive Panda Pokes, which notify you when you’ve been slouching for an extended period of time. 

You can quickly gauge which of your activities are most harmful for your posture by tracking whether you are at home, playing a musical instrument, doing some sport or sleeping. These modes adjust the notification sensitivities so that you don’t get a Panda Poke when you’re fast asleep.

By setting activity selection to Auto, the app will automatically set mode for you, in our current prototype our compass sensor switches between home and sleep mode on its own.


## Technical Details:

### Hardware 

![Circuit Diagram of Bamboo](Hardware_circuit.png)

In Bamboo, the main sensor is a Flex sensor where its resistance increases as the sensor's curvature increases. This enable us to measure the curvature of user's neck/upper back and inform the user if the user is slouching too much. Since the flex sensor is analog, an additional op-amp (TL072CP) and an ADC (ADS1115) are used alongside the flex sensor to enable complete i2c communication with Pi Zero. 

Besides the main sensor, a additional 3D magnetometer (MLX 90393) is used to tell if the user is currently lying down or standing/sitting upright. This provides further information to the application, enabling feature such as auto-switching between modes. 

These two slave sensor are then connected to the master Pi Zero via i2c communication. Pi Zero will handle the next step of preprocessing of raw sensor data and communication with application via Mqtt broker. 

### Connection (Mqtt broker)
... TODO: Chris

### Application
Mobile App Git Link: https://github.com/zenasgram/Bamboo

The application was built using Google's reactive programming language Flutter.

#### Directory Layout

    .
    ├── android                           # Android environment configuration files
    ├── assets                            # 3D object source files
    ├── images                            # Rendered png source files (Human & Bamboo Models)
    ├── ios                               # iOS environment configuration files
    ├── lib                               # Top library
    │   ├── components            
    │   │   └── rounded_button.dart       # Refactored code for registration/login button design
    │   ├── models                 
    │   │   ├── mqtt.dart                 # MQTT listening client code
    │   │   └── simulator.dart            # Real-Time firebase code (used for data backup) + software data simulator
    │   ├── screens                     
    │   │   ├── home_screen.dart          # Code for primary UI screen (including the four modes: Home, Music, Sports, Sleep)
    │   │   ├── login_screen.dart         # Code for login - includes Firebase authentication code
    │   │   ├── registration_screen.dart  # Code for registration - includes Firebase authentication code
    │   │   └── welcome_screen.dart       # Code for initial screen on application boot
    │   │  
    │   ├── main.dart                     # Main script that navigates to screens
    │   └── constants.dart                # Source file that stores dictionaries (threshold, sensitivity map, etc.) and constants
    ├── test
    ├── pubspec.yaml                      # Package files (firebase, firestore, syncfusion charts, etc.)
    └── README.md


![Welcome Screen](Welcome_Screen.png)
![Registration Screen](Registration_Screen.png)
![Login Screen](Login_Screen.png)
![Home Screen](Home_Screen.png)


## Credits:

Zenas (https://github.com/zenasgram), Chris (https://github.com/ChrisDeverall), CK (https://github.com/chikeen) at Imperial College London 2020
