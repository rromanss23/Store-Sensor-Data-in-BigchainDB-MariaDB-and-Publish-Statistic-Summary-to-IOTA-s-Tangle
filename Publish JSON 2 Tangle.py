"""
Programm that code JSON messages to trinary and send them to IOTA's Tangle
"""

import iota, time, json, datetime
from datetime import datetime
from iota import Address, ProposedTransaction, Tag, Transaction, Iota, TryteString


SEED = 'TRYSOMENICESEEDTHATFITSEIGHTYONECHARACTERSLOVEIOC9AIT9M9DUECVHOWNNBARMXR9BNSESLLKWVRWBPMRSR'
######DO NOT NEED TO BEE THE SEED OF THE "TO" ADDRESS ###########################

#GENERATE AN ADDRESS FROM A SEED. SEED CAN BE DIFFERENT FROM ABOVE.THIS ADDRESS HAS TO BE ATTACHED TO THE TANGLE. 
#THIS CAN BE DONE IN THE WALLET.
#GENERATE ADDRESS WITH CHECKSUM
ADDRESS = 'TYRYSOMENICEADDRESSTHATFITSLOVEGSFNEYFODWPIDHTXCGNHKAAWKUVIRANAHTQFCHQOUUX9NKVMLAXUFDQJSBCA' 
tag = iota.Tag('MS') #Tag for in the message.
data = [] #Empty container for pm 10, pm25 data to send to IOTA

#Fill container with sensor data
data.append({'name': 'RomansTest', 'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Temp': 30,'Press': 920})
print("-"*35) 
print ('String data:',json.dumps(data))
trytes = TryteString.from_string(json.dumps(data))
print('Message send to tangle:',trytes.decode())

#api = Iota('http://node02.iotatoken.nl:14265/', SEED) # POW node
api = Iota('http://nodes.iota.fm:80/', SEED) #POW node #################### SEED IS NEEDED TO DO THE SIGNING
print('sleep...')
time.sleep(2)
print(api)
t0 = time.time()
api.send_transfer(
  depth = 3, #the starting point for the random walk. the higher the value, the farther back in the tangle the RW will start. and the longer runtime of the RW. 
  # a typical value, used in wallets is 3 - which starts the RW 3 milestones back
  transfers = [
    ProposedTransaction(
      # Recipient of the transfer.
      address =  Address(ADDRESS),######### ADDRESS WHERE THE DATA GOES
      value = 0,
      tag = tag,
      message = trytes,
    ),
  ],
)
t1 = time.time()
print('Time:',datetime.now().strftime('%H:%M:%S'),' transfer data! in:', round((t1 - t0),1 ), 'seconds ')
