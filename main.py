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

# Will be called upon reception of CONNACK response from the server.
def on_connect(client, data, flags, rc):
    client.subscribe("GaragePi/main_interior_door_toggle", 1)

def on_message(client, data, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set the username to 'token:CHANNEL_TOKEN' before calling connect
client.username_pw_set("token:" + os.environ['MQTT_CHANNEL_TOKEN'])
# Alternatively, set the username to your SECRET KEY
#client.username_pw_set('YOUR_SECRET_KEY')
client.connect("mqtt.beebotte.com", 1883, 60)

client.loop_start()

while 1:
# Publish a message every second
    client.publish("GaragePi/main_interior_door_toggle", "{\"data\": true}", 1)
    time.sleep(1)

