"""
MQTT client for sensor data, computes a temporal statistic summary and publish it to IOTA's tangle

Summary's format is as follows: {"NumMeasurements":int, "Parameter1":[mean, std, min, median, max]}

It has been set up this way due to the message's content length limitation to 2187 Trytes, with proper changes would be shown as:

"Pressure":
"count": 5
"mean": 942.471
"std": 0.027
"min": 942.439
"50%": 942.475
"max": 942.51


"""


from iota import Address, ProposedTransaction, Tag, Transaction, Iota, TryteString, json
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

mqtt_broker = "IPaddress"

sub_topic = "SUBSCRIPTIONTOPIC"

pub_topic = "PUBLICATIONTOPIC"

##### IOTA SETTINGS #####

SEED = 'PUTYOURSEEDHERE99999999999999999999999'
api = Iota('http://173.212.218.8:14265/', SEED)                # POW node, SEED IS NEEDED TO DO THE SIGNING
tag = iota.Tag('PUTYOURTAG')                                   # Tag for in the message.
address = api.get_new_addresses(0, 1)['addresses']             # Generates a list of 1 address
DELAY = XXX                                                    # Time betwwen each summary's computation and sending

##### PANDAS DATA FRAME SET #####

data_frame = pd.DataFrame()

##### MQTT SUBSCRIPTION #####

def on_connect(client, userdata, flags, rc):
    global first_message
    
    print("Connected with result code "+str(rc))
    print ("IOTA address used is " + str(Address(address[0],))) # Prints address generated
    client.subscribe(sub_topic)
    first_message = True
    
def on_message(client, userdata, msg):
    global data_frame
    global first_message 
    
    data_decoded = json.loads(msg.payload)                             # Converts MQTT payload to string
    df1 = pd.DataFrame([data_decoded], columns = data_decoded.keys())  # Insert payload into a Pandas data frame
    data_frame = pd.concat([data_frame, df1])                          
    print(data_frame)
    
    if first_message:
        thread.start()
        first_message = False
    
def wait_time():
    while True:
        time.sleep(DELAY)
        send_summary()
    
def send_summary():
    global data_frame
    new_data = {}
    
    ## IOTA'S IMPLEMENTATION
    data_summary = data_frame.describe([]).round(4)
    print(data_summary)
    
    dict_summary = data_summary.to_dict()
    
    for key,value in dict_summary.items():             # Get rid of reiterative index that increments innecesary messages length
        new_data["Num"] = int(value.pop("count"))
        new_data[key] = list(value.values())
    
    data_frame = pd.DataFrame()  
    
    json_summary = json.dumps(new_data)                # Converts summary to a json object
    print(json_summary)
    print(len(json_summary))
    
    trytes = TryteString.from_string(json_summary)     # Code Json data in trytes
    
    print('Message sent to tangle:',trytes.decode())   # shows decoded msg sent to tangle 

    print('sleep...')
    time.sleep(1)
    
    print(api)
    
    t0 = time.time()
    
    # Sends message
    api.send_transfer(
        depth = 3,
        transfers = [ProposedTransaction(address =  Address(Address(address[0],)),  
          value = 0,
          tag = tag,
          message = trytes,),],)   
    
    t1 = time.time()
    
    #Shows how much it took to send the message to the tangle
    print('Time:',time.strftime('%H:%M:%S', time.localtime()),' data transfered! in:', round((t1 - t0),1 ), 'seconds ')
    
### THREAD FOR COMPUTING AND SENDING DATA SUMMARY ###    

thread = threading.Thread(target = wait_time)

### MQTT INITIALIZER ###
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, 1883, 60)

client.loop_forever()
