# 🔔 Smart Doorbell

## Project Overview
Smart Doorbell is a Raspberry Pi IoT project that simulates a doorbell system. Pressing the SenseHAT joystick triggers the Pi camera to capture a photo of the visitor, uploads it to Cloudinary, and publishes an event (photo URL, temperature, timestamp) via MQTT. A Flask web dashboard subscribes to the MQTT topic and displays the last visitor photo and event details in real time.

## Features
- Press the SenseHAT joystick to trigger the doorbell
- Pi camera captures a photo of the visitor and saves it locally
- Photo uploaded to Cloudinary and stored with a consistent public URL
- SenseHAT temperature reading included in each event payload
- Event published to an MQTT topic via the HiveMQ public broker
- Flask web dashboard subscribes to MQTT and updates automatically on new events
- Last visitor photo, temperature, and timestamp displayed on the dashboard
- State persisted to `doorbell.json` so the dashboard survives restarts

## Tech Stack
| Category | Technology |
|---|---|
| Language | Python 3 |
| Hardware | Raspberry Pi, SenseHAT, Pi Camera |
| Web Framework | Flask |
| Messaging | MQTT (HiveMQ public broker) |
| Image Storage | Cloudinary |
| Camera Library | Picamera2 |

## Project Structure
```
smart-doorbell/
├── state/
│   └── doorbell.json         # Persisted state (last event)
├── static/
│   └── last_visitor.jpg      # Most recent captured image
├── templates/
│   └── status.html           # Flask dashboard template
├── doorbell_camera.py        # Runs on Pi — joystick, camera, MQTT publish
├── upload_cloudinary.py      # Uploads image to Cloudinary
├── web_dashboard.py          # Flask app — MQTT subscribe, serves dashboard
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup Instructions

### Prerequisites
- Raspberry Pi with SenseHAT and camera module attached
- Python 3 installed
- A [Cloudinary](https://cloudinary.com/) account — note your cloud name, API key, and API secret

### Installation
1. Clone the repository:
```bash
git clone https://github.com/rachel-gillespie/smart-doorbell
cd smart-doorbell
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root using `.env.example` as a guide:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## How to Run
In two separate terminals:
```bash
python3 doorbell_camera.py
python3 web_dashboard.py
```

The dashboard will be available at `http://<your-pi-ip>:8000`.

Press the SenseHAT joystick (centre) to trigger the doorbell.

## Reference List
- Cloudinary Python SDK — [Cloudinary docs](https://cloudinary.com/documentation/python_integration)
- Paho MQTT Python client — [Eclipse Paho docs](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)
- Picamera2 — [Picamera2 docs](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- SenseHAT — [SenseHAT docs](https://sense-hat.readthedocs.io/en/latest/)
- Flask — [Flask docs](https://flask.palletsprojects.com/)
- HiveMQ public broker — [HiveMQ](https://www.hivemq.com/public-mqtt-broker/)
