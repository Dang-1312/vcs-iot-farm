# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

import time
import json
import threading

# Import my code
import control_watering as control
import read_wd5 as wd5


# Initialize a counter variable and a thread for event handling
received_count = 0
received_all_event = threading.Event()

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = ".amazonaws.com"
CLIENT_ID = "RasPi_Up"
PATH_TO_CERTIFICATE = "-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = ".pem"
TOPIC = "raspi/publish"

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )

# Update ideal_data and pump system operation
def received(topic, payload, **kwargs):
    msg = json.loads(payload.decode("utf-8"))
    




# Main loop program
while True:
    # Connect to AWS IoT Core
    connect_future = mqtt_connection.connect()
    print("Connecting...")
    # Wait until the MQTT connection is established 
    connect_future.result()
    print("Connected!")
    
    # Subcribe topic "django/request"
    mqtt_connection.subscribe(TOPIC,qos=mqtt.QoS.AT_LEAST_ONCE,callback=received)
    received_all_event.wait()
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()