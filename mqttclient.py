import paho.mqtt.client as mqtt
from tobdb import send_to_bdb
from tomysql import store_mysql
from toiota import send_to_tangle
import json

### MQTT SETTINGS ###

mqtt_broker = "192.168.1.108"  # MQTT broker IP Adress

mqtt_port = 1883  # MQTT port

sub_topic = "test/data"  # receive messages on this topic

pub_topic = "test/instrutions"  # send messages to this topic


### WHEN CONNECTION IS DONE ###

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(sub_topic)
    


### WHEN RECIEVING A MESSAGE ###

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    sensor_data = json.loads(msg.payload)

# Send data to BigchainDB Client
    send_to_bdb(sensor_data)

# Send data to MariaDB client
    store_mysql(sensor_data)
    
# Send data to IOTA's Tangle
    send_to_tangle(sensor_data)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

### Start the MQTT forever loop
client.loop_forever()
