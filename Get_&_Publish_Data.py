##### Libraries #####
from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

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
DELAY=5

##### MQTT Settings#####
Broker = "192.168.1.107"    # Raspberry Pi's IP adress

sub_topic = "test/instructions"    # receive messages on this topic

pub_topic = "test/data"       # send messages to this topic


##### Functions #####
def  header_setup():
    header =[]
    if TEMP_H:
        header.append("temp_h")
    if TEMP_P:
        header.append("temp_p")
    if HUMIDITY:
        header.append("humidity")
    if PRESSURE:
        header.append("pressure")
    if ORIENTATION:
        header.extend(["pitch","roll","yaw"])
    if MAG:
        header.extend(["mag_x","mag_y","mag_z"])
    if ACCELERATION:
        header.extend(["accel_x","accel_y","accel_z"])
    if GYRO:
        header.extend(["gyro_x","gyro_y","gyro_z"])
    header.append("timestamp")

    return header



def get_sense_data():
    sense_data=[]

    if TEMP_H:
        sense_data.append(sense.get_temperature_from_humidity())

    if TEMP_P:
        sense_data.append(sense.get_temperature_from_pressure())

    if HUMIDITY:
        sense_data.append(sense.get_humidity())

    if PRESSURE:
        sense_data.append(sense.get_pressure())

    if ORIENTATION:
        o = sense.get_orientation()
        yaw = o["yaw"]
        pitch = o["pitch"]
        roll = o["roll"]
        sense_data.extend([pitch,roll,yaw])

    if MAG:
        mag = sense.get_compass_raw()
        mag_x = mag["x"]
        mag_y = mag["y"]
        mag_z = mag["z"]
        sense_data.extend([mag_x,mag_y,mag_z])

    if ACCELERATION:
        acc = sense.get_accelerometer_raw()
        x = acc["x"]
        y = acc["y"]
        z = acc["z"]
        sense_data.extend([x,y,z])

    if GYRO:
        gyro = sense.get_gyroscope_raw()
        gyro_x = gyro["x"]
        gyro_y = gyro["y"]
        gyro_z = gyro["z"]
        sense_data.extend([gyro_x,gyro_y,gyro_z])

    sense_data.append(datetime.now())

    return sense_data


def display_sensehat(message):
    sense.show_message(message)


##### MQTT Section #####

# when connecting to mqtt do this

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)
    client.publish(pub_topic, str(header_setup()))

# when receiving a mqtt message do this

def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic + " " + message)
    display_sensehat(message)

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_start()

while True:
    client.publish(pub_topic, str(get_sense_data()))
    time.sleep(DELAY)
            
