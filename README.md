# Uploading-sensor-data-to-IOTA-tangle

## Overview:

This is the repository of my end of dregree project wich consist in the following:
  
  - Collecting data from a sense HAT attached to a Raspberry Pi 3 B+
  - Publish data via MQTT to a Linux machine where there is installed a light weight IOTA wallet, and runs two listening clients
    - The first one stores data in a MySQLdb data base
    - The second on computes temporal data summary and publish it to the IOTA tangle

The aim of this project is to implement the increasingly demanded technology of the Internet of Things (IoT) with blockchain technologies, and build a completely dezentralized sensor system. For this porpouse I have chosen the cryptocurrency IOTA as it provides a fast, secure, free and decentralized way of storing and publishing data and BigchainDB as decentralized database that will took up the place of MySQLdb.
