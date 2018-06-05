# Uploading-sensor-data-to-IOTA-tangle

## Overview:

This is the repository of my end of dregree project wich consist in the following:
  
  - Collecting data from a sense HAT attached to a Raspberry Pi 3 B+
  - Publish data via MQTT to a Linux machine where there is installed a light weight IOTA wallet, and runs three listening clients
    - The first one stores data in a MySQLdb data base
    - The second on computes temporal data summary and publish it to the IOTA tangle
    - The third one stores data in BigchainDB

The aim of this project is to implement the increasingly demanded technology of the Internet of Things (IoT) with blockchain technologies, and build a completely dezentralized sensor system. For this porpouse I have chosen the cryptocurrency IOTA as it provides a fast, secure, free and decentralized way of storing and publishing data and BigchainDB as decentralized database that will took up the place of MySQLdb.

## How to Use the Code:

### 1º) Run pubsensordata.py in your Raspberry Pi: 
It will collect sensor data from the Sense Hat and publish it via MQTT. You need to put your specific credentials, IP addresses and the Publish topics. You can also select which parameters to sense by changing the state of the settings from True to False. You can also adjust the frequency of the data's collection in the variable DELAY.

### 2º) Run mqtt.py in your client machine:
There, you'll need to have in the same directory the rest of the programms: mqtt.py, toiota.py, tobdb.py and tomysql.py. Running mqtt.py will connect to the chosen topic in the 1º) for each message recieved, will simultaneously:
    - Store it in a mysqldb database (previously configured and with the appropiate credentials)
    - Store it in BigchainDB server (previously configured and with the apporpiae credentials)
    - Compute and send a temporal statistics data summary to IOTA's tangle. The summary is an abreviated version from this format: 
    
    "Pressure":"count": 5, "mean": 942.471, "std": 0.027, "min": 942.439, "50%": 942.475, "max": 942.51
    
    To this format:
    
    "Pressure": [5, 942.5349, 0.0207, 942.5166, 942.5283, 942.5625]
 
     Note: It's abbreviated in this way due to the limitations in regards to the capacity of the length of the messages published to the tangle. It's 81 trytes length ~ 2140 carachters.
