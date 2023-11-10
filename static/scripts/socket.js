const Sensors = {};

$(document).ready(async function () {
    // Should fetch the initial data before listening to websocket
    const initRes = await fetch("/get-data", {
        method: "GET",
        credentials: "include",
    });

    if (initRes.status !== 200) return console.error("Failed to fetch initial data");
    const data = await initRes.json();

    // Set the initial values
    StateFunctions.updateDHT({
        temperature: data.sensors.temperature,
        humidity: data.sensors.humidity,
    });

    StateFunctions.updateLightIntensity(data.sensors.light_intensity);
    StateFunctions.updateDevices(data.sensors.devices);

    // Set other data
    StateFunctions.updateUser(data.user);
    StateFunctions.updateLight(data.states.light);
    StateFunctions.updateFan(data.states.fan);
    StateFunctions.updateRSSI(data.config.rssi_threshold);

    if (data.user) {
        StateFunctions.updateFavourites(data.user.favourites);
    }

    // Start listening to socket events
    const socket = io();
    document._socket = socket;

    socket.on("dht_update", (data) => StateFunctions.updateDHT(data));
    socket.on("light_intensity_update", (data) => StateFunctions.updateLightIntensity(data));
    socket.on("devices_update", (data) => StateFunctions.updateDevices(data));

    socket.on("light_update", (status) => StateFunctions.updateLight(status));
    socket.on("fan_update", (status) => StateFunctions.updateFan(status));
    socket.on("user_update", (user) => StateFunctions.updateUser(user));

    State._initialized = true;
});