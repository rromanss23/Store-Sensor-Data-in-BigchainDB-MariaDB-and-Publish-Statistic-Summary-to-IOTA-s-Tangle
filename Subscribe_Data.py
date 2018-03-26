  GNU nano 2.8.6                                                       Archivo: DataSub.py                                                                    

import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import csv
import datetime

Broker = "192.168.1.107"   # Raspberry Pi's IP adress

sub_topic = "test/data"    # receive messages on this topic

pub_topic = "test/instructions"               # send messages to this topic


# mqtt section

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    data = []
    for i in range(16):
        data.append(eval(msg.payload)[i])
    print(msg.topic+" "+str(data))
    csvwriter.writerow(data)
    csvfile.flush()
    print('Writing data to csv')
    publish_mqtt("Logging Data")

# to send a message

def publish_mqtt(sensor_data):
    mqttc = mqtt.Client(pub_topic)
    mqttc.connect(Broker, 1883)
    mqttc.publish(pub_topic, "OK")
   


