const Sensors = {};

$(document).ready(async function () {
    // Start listening to websocket
    const socket = io();

    socket.on("sensor_update", (data) => {
        // Update the fields
        $("#sensor-temp-val").attr("iot-val", data.temperature);
        $("#sensor-hum-val").attr("iot-val", data.humidity);
        $("#sensor-light-val").attr("iot-val", data.light_intensity);
        $("#sensor-devices-val").attr("iot-val", data.devices);

        $("#sensor-temp-val > span").text(roundTwoDecimals(data.temperature));
        $("#sensor-hum-val > span").text(roundTwoDecimals(data.humidity));
        $("#sensor-light-val > span").text(numberWithCommas(data.light_intensity));
        $("#sensor-devices-val > span").text(numberWithCommas(data.devices));

        // Update arrows
        Favourites.updateArrows();
    });
});