const State = {
    sensors: {
        temperature: 0,
        humidity: 0,
        light_intensity: 0,
        devices: 0,
    },
    user: false,
    favourites: {
        temperature: 0,
        humidity: 0,
        light_intensity: 0,
    },
    light: false,
    fan: false,
};

/**
 * Will be accessed by other functions to update the state
 */
class StateFunctions {
    static updateSensors(data) {
        // Update state
        State.sensors.temperature = data.temperature;
        State.sensors.humidity = data.humidity;
        State.sensors.light_intensity = data.light_intensity;
        State.sensors.devices = data.devices;

        // Update displays
        $("#sensor-temp-val").text(roundTwoDecimals(State.sensors.temperature));
        $("#sensor-hum-val").text(roundTwoDecimals(State.sensors.humidity));
        $("#sensor-light-val").text(numberWithCommas(State.sensors.light_intensity));
        $("#sensor-devices-val").text(numberWithCommas(State.sensors.devices));

        // Update arrows
        Favourites.updateArrows();
    }

    static updateFavourites(data) {
        // Update state
        State.favourites.temperature = data.temperature;
        State.favourites.humidity = data.humidity;
        State.favourites.light_intensity = data.light_intensity;

        // Update displays
        $("#fav-temp-val").text(roundTwoDecimals(State.favourites.temperature));
        $("#fav-hum-val").text(roundTwoDecimals(State.favourites.humidity));
        $("#fav-light-val").text(numberWithCommas(State.favourites.light_intensity));

        // Update values
        $("#fav-temp-input").val(State.favourites.temperature);
        $("#fav-hum-input").val(State.favourites.humidity);
        $("#fav-light-input").val(State.favourites.light_intensity);

        // Update arrows
        Favourites.updateArrows();
    }

    static updateUser(user) {
        // Update state
        State.user = user;

        // TODO: Change some visibility stuff
        if (State.user) {
            $(".login-required").removeClass("login-required");
            $(".login-none").css("display", "none");

            $("#user-pfp").attr("src", State.user.avatar);
            $("#user-name").text(State.user.name);
            $("#user-desc").text(State.user.description);
        }
    }

    static updateLight(status) {
        // Update state
        State.light = status;

        // Update displays
        State.light ? LED.setOn() : LED.setOff();
    }

    static updateFan(status) {
        // Update state
        State.fan = status;

        // Update displays
        State.fan ? Fan.setOn() : Fan.setOff();
    }
}