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
    StateFunctions.updateSensors(data.sensors);
    StateFunctions.updateUser(data.user);
    StateFunctions.updateLight(data.states.light);
    StateFunctions.updateFan(data.states.fan);

    if (data.user) {
        StateFunctions.updateFavourites(data.user.favourites);
    }

    // Start listening to socket events
    const socket = io();
    document._socket = socket;

    socket.on("sensor_update", (data) => StateFunctions.updateSensors(data));
    socket.on("light_update", (status) => StateFunctions.updateLight(status));
    socket.on("fan_update", (status) => StateFunctions.updateFan(status));
});