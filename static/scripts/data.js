const State = {
    _initialized: false,
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
    rssi_threshold: -50,
    light: false,
    fan: false,
};

/**
 * Will be accessed by other functions to update the state
 */
class StateFunctions {
    static updateDHT(data) {
        // Update state
        State.sensors.temperature = data.temperature;
        State.sensors.humidity = data.humidity;

        // Update displays
        $("#sensor-temp-val").text(roundTwoDecimals(State.sensors.temperature));
        $("#sensor-hum-val").text(roundTwoDecimals(State.sensors.humidity));

        // Update gradients
        const tempPercentage = Math.min(inverseLerp(State.sensors.temperature, 0, 50), 1);
        const humPercentage = Math.min(inverseLerp(State.sensors.humidity, 0, 100), 1);

        $("#gradient_temp > stop").attr("offset", tempPercentage);
        $("#bar_temp").css("width", tempPercentage * 100 + "%");

        $("#gradient_hum > stop").attr("offset", humPercentage);
        $("#bar_hum").css("width", humPercentage * 100 + "%");

        Favourites.updateArrows();
    }

    static updateLightIntensity(data) {
        // Update state
        State.sensors.light_intensity = data ?? 0;

        // Update displays
        $("#sensor-light-val").text(numberWithCommas(State.sensors.light_intensity));

        // Update gradients
        const lightPercentage = Math.min(inverseLerp(State.sensors.light_intensity, 0, 1024), 1);
        $("#gradient_light > stop").attr("offset", lightPercentage);
        $("#bar_light").css("width", lightPercentage * 100 + "%");

        Favourites.updateArrows();
    }

    static updateDevices(data) {
        // Update state
        State.sensors.devices = data ?? 0;

        // Update displays
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

        if (State.user) {
            // Show the loading animation
            $("#user-loaded").removeClass("d-flex").addClass("d-none");
            $("#user-loading").removeClass("d-none").addClass("d-flex");

            setTimeout(() => {
                // Hide the loading animation
                $("#user-loading").removeClass("d-flex").addClass("d-none");
                $("#user-loaded").removeClass("d-none").addClass("d-flex");

                $(".login-required").css('display', "block");

                $("#user-pfp").attr("src", State.user.avatar);
                $("#user-name").text(State.user.name);
                $("#user-desc").text(State.user.description);
            }, 250);

            if (State._initialized) {
                // Change the favourites
                StateFunctions.updateFavourites(State.user.favourites);

                return sendNotif("success", "Logged in", `Welcome, ${State.user.name}!`)
            }
        } else {
            $(".login-required").css('display', "none");

            $("#user-name").text("Please scan your ID card");
            $("#user-desc").text("You are not logged in. Please log in to access a large range of features, such as managing your favourite configuration.");

            if (State._initialized) {
                return sendNotif("error", "Logged out", "You have been logged out.");
            }
        }
    }

    static updateLight(status) {
        // Update state
        State.light = status;

        // Update displays
        LED.setState(State.light);

        // Update the "email sent" label
        if (State.light) {
            $("#light-sent-label").text("Email has been sent!");
        } else {
            $("#light-sent-label").text("");
        }
    }

    static updateFan(status) {
        // Update state
        State.fan = status;

        // Update displays
        Fan.setState(State.fan);
    }

    static updateRSSI(value) {
        // Update state
        State.rssi_threshold = value;

        // Update displays
        $("#rssi-input").val(State.rssi_threshold);
    }
}