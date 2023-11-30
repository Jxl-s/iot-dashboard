const SEND_DELAY = 5 * 1000; // 5 seconds
const DISCONNECT_DELAY = 10 * 1000; // No packet for 10 seconds => disconnect

const BarnowlHci = require("barnowl-hci");
const mqtt = require("mqtt");
const Raddec = require("raddec");

// Await for a mqtt connection to happen
const client = mqtt.connect("mqtt://0.0.0.0:1883");
client.on("connect", () => {
    console.log("[Bluetooth] Connected to broker!");

    // Add the listener
    const barnowl = new BarnowlHci();
    barnowl.addListener(BarnowlHci.SocketListener, {});

    // Listen to events
    const bluetoothDevices = {}
    barnowl.on('raddec', function (raddec) {
        const flattened = raddec.toFlattened();
        if (flattened.transmitterIdType !== Raddec.identifiers.TYPE_RND48) return;

        // In situations where values are missing, use defaults
        bluetoothDevices[flattened.transmitterId] = [flattened.rssi ?? -1000, flattened.timestamp ?? Date.now()];
    });

    // Purge and print the map each interval
    setInterval(() => {
        // Disconnect devices that didn't send any recent packet
        const timeNow = Date.now();
        const keysToDelete = [];

        for (const [key, value] of Object.entries(bluetoothDevices)) {
            if (timeNow - value[1] > DISCONNECT_DELAY) {
                keysToDelete.push(key);
            }
        }

        // Remove the entries outside the loop
        for (const key of keysToDelete) {
            delete bluetoothDevices[key];
        }

        // Make a new array only containing unique RSSI's
        const rssiArray = Object.values(bluetoothDevices).map((value) => value[0]);

        // Send it through MQTT
        console.log(`[Bluetooth] Sending RSSI array ... (${rssiArray.length} devices)`)
        client.publish("room/devices", JSON.stringify(rssiArray));
    }, SEND_DELAY);
});