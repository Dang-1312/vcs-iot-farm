import time
# from paho.mqtt import client as mqtt_client
import paho.mqtt.publish as publish
# import psutil
import string
import logging

# Channel ID.
channel_ID = "2193827"

# API Key write
apiKey = "LSYSZNK2VG2ADI6W"

useUnsecuredTCP = False

useUnsecuredWebsockets = False

useSSLWebsockets = True

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "MhsLMCYkCQArLDkfNQ4xCi8"
mqtt_username  = "MhsLMCYkCQArLDkfNQ4xCi8"
mqtt_password  = "3wKBSoL7pZl2qI0kFqCMo8Ws"

tTransport = "websockets"
tPort = 80

# Create the topic string.
topic = "channels/" + channel_ID + "/publish"

def publish_data(data):
            
    # Creat data
    mois_soil = data["Moisture_soil"]
    temp_soil = data["Temperature_soil"]
    ec = data["EC"]
    nito = data["Soil_nitrogen"]
    photpho = data["Soil_phosphorus"]
    kali = data["Soil_potassium"]
    pH = data["pH"]
    co2 = data["CO2"]
    temp_air = data["Temp_air"]
    hum_air = data["Hum_air"]
        
    tPayload = "field1=" + str(mois_soil) + "&field2=" + str(ec) + "&field3=" + str(temp_soil) + "&field4=" + str(nito) + "&field5=" + str(pH) + "&field6=" + str(co2) + "&field7=" + str(temp_air) + "&field8=" + str(hum_air)
    
    print(tPayload)
    
    try:
        logging.info("Publishing")
        publish.single(topic, payload=tPayload, hostname=mqtt_host, transport=tTransport, port=tPort, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
        time.sleep(5)
        tPayload = "&field4=" + str(photpho)
        publish.single(topic, payload=tPayload, hostname=mqtt_host, transport=tTransport, port=tPort, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
        time.sleep(5)
        tPayload = "&field4=" + str(kali)
        publish.single(topic, payload=tPayload, hostname=mqtt_host, transport=tTransport, port=tPort, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
        return "Success"
    
    except (KeyboardInterrupt):
        print("Measurement has been cancelled.")
        return "Cancel"

    except Exception as error: 
        print ("There was an error while publishing the data.")
        return {type(error).__name__} - {error}