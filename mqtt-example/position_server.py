#!/usr/bin/env python3

import json
import paho.mqtt.client as mqtt

# Tag config. Configured tag-ids will be replaced by their name
# <ID>: <Name>
tag_config = {
    'cafe060087081425': '10-1F',
    '1234568': '10-1M',
    '1234569': '10-2M',
}

# Initialize dictionaries for received messages
iloc_dict = {}
poi_dict = {}


def create_floor_dict(pos_dict, topic):
    """
    function to create a floor based dictionary
    """

    # initialize empty floor dictionary
    floor_dict = {
        'topic': topic.split('/')[-1],  # remove celidon/ from topic
        'floor-1': {},
        'floor0': {},
        'floor1': {},
        'floor2': {},
        'unknown': {}  # values outside of floor range
    }

    # map received positions to floors (based on z position)
    for key, value in pos_dict.items():
        if -2.76 <= value['pos'][2] < 0:
            floor_dict['floor-1'][key] = value
        elif 0 <= value['pos'][2] < 3.510:
            floor_dict['floor0'][key] = value
        elif 3.510 <= value['pos'][2] < 6.520:
            floor_dict['floor1'][key] = value
        elif 6.520 <= value['pos'][2] < 9.530:
            floor_dict['floor2'][key] = value
        else:
            floor_dict['unknown'][key] = value

    return floor_dict


# define mqtt callbacks
def on_message(mqtt_client, userdata, msg):
    """
    callback to handle received mqtt messages
    """
    global iloc_dict, poi_dict  # setup global variables
    # decode received mqtt message based on topic
    if msg.topic == 'celidon/iloc':
        recv_data = json.loads(msg.payload.decode())

        # add received data to position dictionary
        for tag_id, data in recv_data.items():
            position_m = [p / 1000 for p in data['pos']]
            iloc_dict[tag_config.get(tag_id, str(tag_id))] = {'ts': data['ts'],
                                                              'pos': position_m}

        floor_dict = create_floor_dict(iloc_dict, msg.topic)
        # log received iloc message
        print(floor_dict)

    elif msg.topic == 'celidon/poi':
        recv_data = json.loads(msg.payload.decode())

        # add received data to position dictionary
        for poi_id, data in recv_data.items():
            position_m = [p / 1000 for p in data['pos']]
            poi_dict[str(poi_id)] = {'ts': data['ts'],
                                     'to': data['to'],
                                     'pos': position_m,
                                     'text': data['text']}

        floor_dict = create_floor_dict(poi_dict, msg.topic)
        # log received poi message
        print(floor_dict)


def on_disconnect(mqtt_client, userdata, rc=0):
    mqtt_client.loop_stop()


# MQTT topics to subscribe to
MQTT_TOPICS = [('celidon/iloc', 0), ('celidon/poi', 0)]

# setup mqtt
# address and port of the MQTT broker.
mqtt_port = 1883  # default mqtt port: 1883
mqtt_broker = 'localhost'  # address of the MQTT broker
mqtt_client = mqtt.Client('CelidonSub')  # name of this MQTT subscriber

# connect to MQTT broker
mqtt_client.connect(mqtt_broker, mqtt_port)

# subscribe to MQTT topics
mqtt_client.subscribe(MQTT_TOPICS)

# configure callback for message reception
mqtt_client.on_message = on_message

# configure callback for disconnection
mqtt_client.on_disconnect = on_disconnect

# start MQTT client loop
mqtt_client.loop_start()
