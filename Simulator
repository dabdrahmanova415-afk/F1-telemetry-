import json
import random
import time
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("mosquitto",1883)

while True:

    telemetry = {
        "car":"Ferrari_16",
        "lap":random.randint(1,70),
        "speed":random.randint(180,340),
        "fuel":round(random.uniform(5,100),2),
        "tire_wear":round(random.uniform(0,1),2)
    }

    client.publish(
        "f1/telemetry",
        json.dumps(telemetry)
    )

    time.sleep(3)


    
