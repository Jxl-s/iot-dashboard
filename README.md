# IoT Dashboard
Project for 420-531-VA (Internet of Things)

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

Run the following terminals simultaneously
1. Bluetooth packet listener
```bash
sudo node ./bluetooth.js
```
2. IoT Dashboard
```bash
python app
```

## To create profiles
Run the following command, and follow the steps and scan your card
```bash
python create_user.py
```