# IoT Dashboard
Project for 420-531-VA (Internet of Things)

## Getting Started
Create a file `.env`, containing the following
```
EMAIL_ADDRESS=<email address>
EMAIL_PASSWORD=<email password>
```

Run the following command to install the required libraries
```bash
pip install -r requirements.txt
```

Then, run the following command to start the application
```bash
python app
```

## To create profiles
Run the following command, and select an image to upload.
Note that if you don't select a profile picture, the default one
will be used. A description is optional.

```bash
python actions.py --create "username here" "description here"
```