#!/usr/bin/python

# Copyright (c) 2013-2014 Beebotte <contact@beebotte.com>
# This program is published under the MIT License (http://opensource.org/licenses/MIT).

############################################################
# This code uses the Beebotte API, you must have an account.
# You can register here: http://beebotte.com/register
#############################################################

import time
import paho.mqtt.client as mqtt
import os
import RPi.GPIO as gpio

CHANNEL="GaragePi"

RESOURCES = {
    "main_interior_door_toggle": 17,
    "main_exterior_door_toggle": 27,
    "secondary_exterior_door_toggle": 22
}

gpio.setmode(gpio.BCM)
for pin in RESOURCES.values():
    gpio.setup(pin, gpio.OUT)
    gpio.output(pin, gpio.HIGH) # HACK: this should be set to HIGH as fast as possible because the pin will start LOW

# Will be called upon reception of CONNACK response from the server.
def on_connect(client, data, flags, rc):
    for name in RESOURCES.keys():
        client.subscribe(CHANNEL + "/" + name)

def pulse(port):
    gpio.output(port, gpio.LOW)
    time.sleep(0.4)
    gpio.output(port, gpio.HIGH)

def on_message(client, data, msg):
    print(msg.topic + " " + str(msg.payload))
    splitted = msg.topic.split("/", 1)
    if len(splitted) < 2:
        return
    channel = splitted[0]
    resource = splitted[1]
    if channel != CHANNEL:
        return
    if resource in RESOURCES:
        pulse(RESOURCES[resource])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set the username to 'token:CHANNEL_TOKEN' before calling connect
client.username_pw_set("token:" + os.environ['MQTT_CHANNEL_TOKEN'])
# Alternatively, set the username to your SECRET KEY
#client.username_pw_set('YOUR_SECRET_KEY')
while True:
    try:
        client.connect("mqtt.beebotte.com", 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        break
    except:
        pass

