#!/usr/bin/env python3
import os, json, time, datetime
from flask import Flask, render_template
import paho.mqtt.client as mqtt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(BASE_DIR, "state")
STATE_PATH = os.path.join(STATE_DIR, "doorbell.json")

app = Flask(__name__, static_folder="static")

# MQTT CONFIG
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "/rachel-gillespie/event/doorbell"  # UPDATE THIS TO YOUR ID

def load_state():
    try:
        with open(STATE_PATH) as f:
            data = json.load(f)
        ts = data.get("ts")
        if not ts:
            return None
        age = int(time.time()) - ts
        time_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        data["age"] = age
        data["time_str"] = time_str
        return data
    except FileNotFoundError:
        return None
    except Exception as e:
        print("Error loading state:", e)
        return None

@app.route("/")
def index():
    last_event = load_state()
    return render_template(
        'status.html',
        last_event=last_event
    )

# --- MQTT CALLBACKS ---

def on_connect(client, userdata, flags, rc):
    print("MQTT connected with result code", rc)
    client.subscribe(MQTT_TOPIC)
    print("Subscribed to:", MQTT_TOPIC)


def on_message(client, userdata, msg):
    print("MQTT message on", msg.topic)
    payload_str = msg.payload.decode("utf-8")
    data = json.loads(payload_str)  
    data["ts"] = int(time.time())
    with open(STATE_PATH, "w") as f:
        json.dump(data, f)
    print("State updated:", data)
   
       
# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()  # run MQTT network loop in background thread

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)