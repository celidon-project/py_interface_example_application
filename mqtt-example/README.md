# Requirements
This example relies on python 3 and the [paho-mqtt](https://pypi.org/project/paho-mqtt/) library.
Furthermore a MQTT broker must be accessible from this machine. If no MQTT broker is available you can install [docker](https://docs.docker.com/install/) on your system and run a MQTT broker with `docker run -ti -p 1883:1883 toke/mosquitto`.


# Run
To run this example either run `python3 position_server.py` (MQTT subscriber) and `python3 position_client.py` (MQTT publisher).


# Expected Output:
Note that the position and time values will vary.

## position_server
```bash
{'topic': 'iloc', 'floor-1': {}, 'floor0': {'10-1F': {'ts': 1587027899739, 'pos': [5.135, 5.032, 2.565]}}, 'floor1': {}, 'floor2': {}}
{'topic': 'iloc', 'floor-1': {}, 'floor0': {'10-1F': {'ts': 1587027899739, 'pos': [5.135, 5.032, 2.565]}, '10-1M': {'ts': 1587027899740, 'pos': [4.602, 4.716, 3.495]}}, 'floor1': {}, 'floor2': {}}
{'topic': 'iloc', 'floor-1': {}, 'floor0': {'10-1F': {'ts': 1587027899739, 'pos': [5.135, 5.032, 2.565]}, '10-1M': {'ts': 1587027899740, 'pos': [4.602, 4.716, 3.495]}, '10-2M': {'ts': 1587027899740, 'pos': [4.617, 4.591, 2.827]}}, 'floor1': {}, 'floor2': {}}
{'topic': 'poi', 'floor-1': {}, 'floor0': {'feed020012341234': {'ts': 1587027899740, 'to': 5000, 'pos': [10.65, 10.5, 1.0], 'text': 'Emergency Exit'}}, 'floor1': {}, 'floor2': {}}

```

## position_client
```bash
{'cafe060087081425': {'ts': 1587027899739, 'pos': [5135, 5032, 2565]}}
{'1234568': {'ts': 1587027899740, 'pos': [4602, 4716, 3495]}}
{'1234569': {'ts': 1587027899740, 'pos': [4617, 4591, 2827]}}
{'feed020012341234': {'ts': 1587027899740, 'to': 5000, 'pos': [10650, 10500, 1000], 'text': 'Emergency Exit'}}
```

