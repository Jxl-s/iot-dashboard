import paho.mqtt.client as mqtt
import time

CONNECTION_ATTEMPTS = 5  # How many times to try connecting
CONNECTION_DELAY = 2  # Seconds to wait between connection attempts


class MQTTClient:
    def __init__(self, host, port, topics):
        # Assign the host and port properties
        self.host = host
        self.port = port
        self.topics = topics

        self._callbacks = {}
        self._callback_datatypes = {}

        # Create a client
        self.client = mqtt.Client()

        # Register events
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    # Allow to add callbacks to the client. Can also set a datatype to try
    # converting the payload into
    def set_callback(self, topic, callback, datatype=str):
        self._callbacks[topic] = callback
        self._callback_datatypes[topic] = datatype

    # Starts the connection loop
    def connect(self):
        # Connection flags
        conn_success = False
        conn_attempts = 0

        # Try until it connects, or until we run out of attempts
        while conn_success is False and conn_attempts < CONNECTION_ATTEMPTS:
            conn_attempts += 1

            try:
                self.client.connect(self.host, self.port, 60)
                self.client.loop_forever()
            except Exception:
                # Try again after a delay
                print(f"[MQTT] Connection failed (attempt {conn_attempts})")
                time.sleep(CONNECTION_DELAY)

    # -- Private methods --
    def _on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] Connected with result code {str(rc)}")

        # Subscribe to provided topics
        client.subscribe(self.topics)

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic in self._callbacks:
            # Try converting the callback type (int, float, ...)
            try:
                payload = self._callback_datatypes[topic](payload)
            except ValueError:
                return

            # If it worked, call the callback
            self._callbacks[topic](payload)
