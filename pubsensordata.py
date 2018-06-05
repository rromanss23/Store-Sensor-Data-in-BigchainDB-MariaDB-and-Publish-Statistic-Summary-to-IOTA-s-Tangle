##### Libraries #####
from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import json

sense = SenseHat()

##### Logging Settings #####
FILENAME = ""
WRITE_FREQUENCY = 100
TEMP_H=True
TEMP_P=False
HUMIDITY=True
PRESSURE=True
ORIENTATION=True
ACCELERATION=True
MAG=True
GYRO=True
DELAY=2

##### MQTT Settings #####
Broker = "localhost"

sub_topic = "test/instructions"    # receive messages on this topic

pub_topic = "test/data"       # send messages to this topic

##### FUNCTIONS #####

def get_sense_data():
    sense_data={}

    if TEMP_H:
        sense_data["Temperature"] = sense.get_temperature_from_humidity()

    if TEMP_P:
        sense_data["Temperature"] = sense.get_temperature_from_pressure()

    if HUMIDITY:
        sense_data["Humidity"] = sense.get_humidity()

    if PRESSURE:
        sense_data["Pressure"] = sense.get_pressure()

    if ORIENTATION:
        o = sense.get_orientation()
        sense_data["Yaw"] = o["yaw"]
        sense_data["Pitch"] = o["pitch"]
        sense_data["Roll"] = o["roll"]

    if MAG:
        mag = sense.get_compass_raw()
        sense_data["Magnetic_Field_x"] = mag["x"]
        sense_data["Magnetic_Field_y"] = mag["y"]
        sense_data["Magnetic_Field_z"] = mag["z"]

    if ACCELERATION:
        acc = sense.get_accelerometer_raw()
        sense_data["Acceleration_x"] = acc["x"]
        sense_data["Acceleration_y"] = acc["y"]
        sense_data["Acceleration_z"] = acc["z"]

    if GYRO:
        gyro = sense.get_gyroscope_raw()
        sense_data["Gyroscope_x"] = gyro["x"]
        sense_data["Gyroscope_y"] = gyro["y"]
        sense_data["Gyroscope_z"] = gyro["z"]

    sense_data["Data_Collection_Time_Stamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    return sense_data

##### MQTT Section #####

# when connecting to mqtt do this

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.connect(Broker, 1883, 60)
client.loop_start()

while True:
    client.publish(pub_topic, json.dumps(get_sense_data()))
    time.sleep(DELAY)
