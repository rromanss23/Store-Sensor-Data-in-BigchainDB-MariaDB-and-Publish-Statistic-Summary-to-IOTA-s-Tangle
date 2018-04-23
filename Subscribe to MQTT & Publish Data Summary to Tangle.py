from iota import Address, ProposedTransaction, Tag, Transaction, Iota, TryteString
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from datetime import datetime
import pandas as pd
import json
import time
import iota
import datetime
import threading

##### MQTT SETTINGS #####

mqtt_broker = "192.168.1.108"

sub_topic = "test/data"

pub_topic = "confirmation"

##### IOTA SETTINGS #####

SEED = ''
ADDRESS = '' #Need to be attached to tangle
tag = iota.Tag('SENSORDATA') #Tag for in the message.
api = Iota('http://173.212.218.8:14265/', SEED) #POW node, SEED IS NEEDED TO DO THE SIGNING

##### PANDAS DATA FRAME SET #####

data_frame = pd.DataFrame()

##### MQTT SUBSCRIPTION #####

def on_connect(client, userdata, flags, rc):
    global first_message
    
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)
    first_message = True
    
def on_message(client, userdata, msg):
    global data_frame
    global first_message 
    
    data_decoded = json.loads(msg.payload)
    df1 = pd.DataFrame([data_decoded], columns = data_decoded.keys())
    data_frame = pd.concat([data_frame, df1])
    print(data_frame)
    
    if first_message:
        thread.start()
        first_message = False
    
def wait_time():
    while True:
        time.sleep(10)
        send_summary()
    
def send_summary():
    global data_frame
    
    ## IOTA'S IMPLEMENTATION
    data_summary = dict(data_frame.describe()) # compute data summary and convert it to dictionary
    data_frame = pd.DataFrame()                # empty data frame
    json_summary = json.dumps(data_summary)    # converts data summary into json 
    
    trytes = TryteString.from_string(json_summary) # Code Json data in trytes
    
    print('Message sent to tangle:',trytes.decode()) # shows decoded msg sent to tangle 

    print('sleep...')
    time.sleep(1)
    
    print(api)
    
    t0 = time.time()
    
    api.send_transfer(
        depth = 3,
        transfers = [ProposedTransaction(address =  Address(ADDRESS),
          value = 0,
          tag = tag,
          message = trytes,),],)
    
    t1 = time.time()
    
    print('Time:',time.strftime('%H:%M:%S', time.localtime()),' data transfered! in:', round((t1 - t0),1 ), 'seconds ')
    
    
### THREAD FOR COMPUTING AND SENDING DATA SUMMARY ###    

thread = threading.Thread(target = wait_time)

### MQTT INITIALIZER ###
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, 1883, 60)

client.loop_forever()
