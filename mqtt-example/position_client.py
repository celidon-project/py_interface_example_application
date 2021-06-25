#!/usr/bin/env python3

import json
import paho.mqtt.client as mqtt
from random import random
import time

# setup mqtt
# address and port of the MQTT broker.
mqtt_port = 1883  # default mqtt port: 1883
mqtt_broker = 'localhost'  # address of the MQTT broker
mqtt_client = mqtt.Client('CelidonPub')  # name of this MQTT publisher

# connect to MQTT broker
mqtt_client.connect(mqtt_broker, mqtt_port)

# MQTT topics to publish messages to
mqtt_iloc_topic = 'celidon/iloc'
mqtt_poi_topic = 'celidon/poi'

# setup example tag_ids and aliases for localization agents
tag_ids = [('cafe060087081425', '10-1F'),
           ('1234568', '10-1M'),
           ('1234569', '10-2M')]

# setup example poi_ids and alias for localization agents
poi_ids = [('feed020012341234', 'poi-123']

# generate random positions
positions_mm = {i: [5000, 5000, 3000] for i in tag_ids}


while True:
    # send iloc messages
    for tag_id, alias in tag_ids:
        # add random walk for each localization agent
        new_pos = []
        for pos in positions_mm[tag_id]:
            random_offset = (random() - 0.5) * 1000  # random offset in mm
            new_pos.append(int(pos + random_offset))  # add random offset
        positions_mm[tag_id] = new_pos

        # get current unix timestamp in ms
        time_ms = int(time.time() * 1000)

        # mqtt message format to send to the position server
        mqtt_iloc_dict = {
            tag_id: {
                'ts': time_ms,
                'pos': positions_mm[tag_id],
                'alias': alias
            }
        }

        # log message
        print(mqtt_iloc_dict)

        # encode and publish message via MQTT at the specified topic
        mqtt_client.publish(mqtt_iloc_topic, json.dumps(mqtt_iloc_dict))

    # send poi messages
    for poi_id, alias in poi_ids:

        # get current unix timestamp in ms
        time_ms = int(time.time() * 1000)

        # mqtt poi message format to send to the position server
        mqtt_poi_dict = {
            poi_id: {
                'ts': time_ms,
                'to': 5000,
                'pos': [10650, 10500, 1000],
                'text': 'Emergency Exit',
                'alias': alias
            }
        }

        # log message
        print(mqtt_poi_dict)

        # encode and publish poi message via mqtt at the mqtt topic
        mqtt_client.publish(mqtt_poi_topic, json.dumps(mqtt_poi_dict))

    # sleep for 1 second
    time.sleep(1)
