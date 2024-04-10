# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

import time
import json

# Import my code
import read_sensors as measure

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

# Main loop program
while True:
    start=time.time()
    
    # Connect to AWS IoT Core
    connect_future = mqtt_connection.connect()
    print("Connecting...")
    # Wait until the MQTT connection is established 
    connect_future.result()
    print("Connected!")
    
    # Measure data from the sensors
    message = measure.value()
    
    # Publish data to AWS IoT Core
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    
    end=time.time()
    wait=300+start-end
    if wait > 0 :
        time.sleep(wait)  
    else:
        time.sleep(10)