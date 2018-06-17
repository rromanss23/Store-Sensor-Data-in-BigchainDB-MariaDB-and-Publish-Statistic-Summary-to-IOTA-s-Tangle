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
import pandas as pd
import json
import time
import iota
import threading

##### IOTA SETTINGS #####

SEED = 'TZ9FAELAEDZRIJBYXJBMNPSKOBUBONNOBF9WURC9AIT9M9DUECVHOWNNBARMXR9BNSESLLKWVRWBPMRSR'
api = Iota('http://173.212.218.8:14265/', SEED)                # POW node, SEED IS NEEDED TO DO THE SIGNING
tag = iota.Tag('RBRRYPISNSRSMRYFRSTVSN')          # Tag for in the message.
address = api.get_new_addresses(0, 1)['addresses']             # Generates a list of 1 address

##### PANDAS DATA FRAME SET #####

data_frame = pd.DataFrame()

######

def send_to_iota(sensor_data, message):
    global data_frame

    data_decoded = sensor_data
    df1 = pd.DataFrame([data_decoded], columns=data_decoded.keys())
    data_frame = pd.concat([data_frame, df1])
    print(data_frame)

    if message:
        thread.start()
        message = False

    return message


def wait_time():
    while True:
        time.sleep(10)
        send_summary()


def send_summary():
    global data_frame
    new_data = {}

    ## IOTA'S IMPLEMENTATION
    data_summary = data_frame.describe([]).round(4)
    print(data_summary)

    dict_summary = data_summary.to_dict()

    for key, value in dict_summary.items():
        new_data["Num"] = int(value.pop("count"))
        new_data[key] = list(value.values())

    data_frame = pd.DataFrame()

    json_summary = json.dumps(new_data)
    print(json_summary)
    print(len(json_summary))

    trytes = TryteString.from_string(json_summary)  # Code Json data in trytes

    print('Message sent to tangle:', trytes.decode())  # shows decoded msg sent to tangle

    print('sleep...')
    time.sleep(1)

    print(api)

    t0 = time.time()

    api.send_transfer(
        depth=3,
        transfers=[ProposedTransaction(address=Address(Address(address[0], )),
                                       value=0,
                                       tag=tag,
                                       message=trytes, ), ], )

    t1 = time.time()

    print(
    'Time:', time.strftime('%H:%M:%S', time.localtime()), ' data transfered! in:', round((t1 - t0), 1), 'seconds ')


### THREAD FOR COMPUTING AND SENDING DATA SUMMARY ###

thread = threading.Thread(target=wait_time)
