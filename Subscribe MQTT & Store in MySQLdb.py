import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import csv
import datetime
import MySQLdb as mdb
import json

##### USER CONFIGURATION & DATABASE SETUP #####

### MQTT SETTINGS ###

mqtt_broker = "IPaddress"          # MQTT broker IP Adress

mqtt_port = 1883                   # MQTT port

sub_topic = "test/data"            # receive messages on this topic

pub_topic = "test/instrutions"     # send messages to this topic


### MYSQL SETTINGS ###

data_base_hostname = "localhost"          # MySQL host ip address or name

data_base_database = "iota"               # MySQL database name

data_base_username = "username"           # MySQL database user name

data_base_password = "password"         # MySQL database password

### MYSQL SETUP ###

data_base = mdb.connect(data_base_hostname,  # connect with MySQL database
                        data_base_username,
                        data_base_password,
                        data_base_database) 

data_base_cursor = data_base.cursor()        # prepare a cursor object

##### HELPER FUNCTIONS #####

### WHEN CONNECTION IS DONE ###

def on_connect(client, userdata, flags, rc):
    
    print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)

### WHEN RECIEVING A MESSAGE ###

def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    vars_to_sql = []
    keys_to_sql = []
    data_list = []
    
    data_list = json.loads(msg.payload)
    
    for key,value in data_list.items():

      if key == 'Data_Storage_Time_Stamp':
        value = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

      vars_to_sql.append(value)
      keys_to_sql.append(key)
    
    keys_to_sql = ', '.join(keys_to_sql)
    
    try:
       # Execute the SQL command 

       queryText = "INSERT INTO Environment_Parameters(%s) VALUES %r"
       queryArgs = (keys_to_sql, tuple(vars_to_sql))
       data_base_cursor.execute(queryText % queryArgs)
       print('Successfully Added record to mysql')
       data_base.commit()
    
    except mdb.Error as e:

        try:

            print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
        except IndexError:

            print ("MySQL Error: %s" % str(e))
            
        # Rollback in case there is any error

        data_base.rollback()

        print('ERROR adding record to MYSQL')


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

### Start the MQTT forever loop
client.loop_forever()
