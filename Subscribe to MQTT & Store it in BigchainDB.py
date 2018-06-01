import time
import paho.mqtt.client as mqtt
from bigchaindb_driver import BigchainDB
import json

##### USER CONFIGURATION & DATABASE SETUP #####

victor_priv = 'yourprivatekey'
victor_pub = 'your public key'

"""
tokens = {}
tokens['app_id'] = 'f6a958f0'
tokens['app_key'] = '34be8a4a2ecd5c1fa0b14cc56ad7481c'

bdb = BigchainDB('https://test.bigchaindb.com', headers=tokens)
"""

bdb_root_url = 'http://localhost:9984'
bdb = BigchainDB(bdb_root_url)

##### Raspberry Data

raspberry_asset = {
    'data': {
        'raspberry pi': {
            'serial_number': 'RPI01',
            'owner': 'UPM'
        },
    },
}

raspberry_asset_metadata = {
    'Environment Parameters': 'Here goes sensor data'
}

### MQTT SETTINGS ###

mqtt_broker = "192.168.1.108"  # MQTT broker IP Adress

mqtt_port = 1883  # MQTT port

sub_topic = "test/data"  # receive messages on this topic

pub_topic = "test/instrutions"  # send messages to this topic

##### HELPER FUNCTIONS #####

### WHEN CONNECTION IS DONE ###

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(sub_topic)


### WHEN RECIEVING A MESSAGE ###

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    sensor_data = json.loads(msg.payload)

    raspberry_asset['data']['raspberry pi']['Storage TimeStamp'] = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    raspberry_asset_metadata = sensor_data

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=victor_pub,
        asset=raspberry_asset,
        metadata=raspberry_asset_metadata
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=victor_priv
    )

    print(fulfilled_creation_tx)

    bdb.transactions.send(fulfilled_creation_tx)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

### Start the MQTT forever loop
client.loop_forever()
