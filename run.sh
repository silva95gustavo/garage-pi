#!/bin/bash

DIRNAME="$(dirname $0)"

export MQTT_CHANNEL_TOKEN="$(cat "$DIRNAME/token.txt")"

python3 "$DIRNAME/main.py"

