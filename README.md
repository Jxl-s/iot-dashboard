# IoT Dashboard

Project for 420-531-VA (Internet of Things)

## Prerequisites

- A Raspberry Pi 4 (or equivalent)
- Python 3.10+
- Node.js 18.0+
- Mosquitto MQTT Broker 2.0+

## Getting Started

Create a file `.env`, containing the following
```
NOTIFICATION_EMAIL=<notification recipient>

EMAIL_ADDRESS=<email address>
EMAIL_PASSWORD=<email password>
```

Run the following commands to install the required libraries

```bash
pip install -r requirements.txt
npm install
```

Make sure that the mosquitto broker is running, then run the following terminals simultaneously (on different terminals)

1. Bluetooth packet listener

```bash
sudo node ./bluetooth.js
```

2. IoT Dashboard

```bash
python app
```
