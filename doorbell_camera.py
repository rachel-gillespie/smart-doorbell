#!/usr/bin/env python3
import time, os
import json
from datetime import datetime
from sense_hat import SenseHat
from picamera2 import Picamera2
from upload_cloudinary import upload_image
import paho.mqtt.client as mqtt

#use os to set up base and static folder 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #get current directory
STATIC_DIR = os.path.join(BASE_DIR, "static") #set static directory path
os.makedirs(STATIC_DIR, exist_ok=True) #create static directory if it doesn't exist
IMAGE_PATH = os.path.join(STATIC_DIR, "last_visitor.jpg") #set image path

sense = SenseHat()
sense.clear(0, 0, 0)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
print("Camera started. Press the Sense HAT joystick (middle) to take a photo.")

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "/rachel-gillespie/event/doorbell"  # change to your own ID

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

STATE_DIR = os.path.join(BASE_DIR, "state")
os.makedirs(STATE_DIR, exist_ok=True)
STATE_PATH = os.path.join(STATE_DIR, "doorbell.json")

def save_state(image_url=None):
    now = datetime.now()
    celcius = round(sense.temperature, 2)
    payload = {
        "celcius": round(celcius, 2),
        "fahrenheit": round(1.8 * celcius + 32, 2),
        "image":image_url,# path to the image file
        "ts": int(now.timestamp()), #seconds since the unix epoch(if you dont know - look it up)
        "iso": now.isoformat(timespec="seconds") #nice, human-readable timestamp string
    }
    with open(STATE_PATH, "w") as f:
        json.dump(payload, f)
    print("State saved:", payload)

    with open(STATE_PATH, 'r') as f:
        payload = json.load(f)
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print("MQTT event published:", payload)

def capture_photo():
    print("Capturing visitor photo...")
    picam2.capture_file(IMAGE_PATH)
    sense.clear(0, 255, 0)  # flash green
    time.sleep(0.3)
    sense.clear(0, 0, 0)
    print("Photo saved to:", IMAGE_PATH)

try:
    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed" and event.direction == "middle":
                print("Doorbell pressed at", datetime.now())
                capture_photo()
                url = upload_image(IMAGE_PATH)
                save_state(url)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    picam2.stop()
    sense.clear()
    client.loop_stop()
    client.disconnect()