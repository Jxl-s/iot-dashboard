const Favourites = {};

const TEMP_TRESHOLD = 1;
const HUM_TRESHOLD = 5;
const LIGHT_TRESHOLD = 50;

Favourites.edit = () => {
    $("#edit-favs-btn").text("Cancel").css("background-color", "#C25B5B");

    // Make the values disappear
    $(".fav-val").addClass("hide");
    $(".fav-input").removeClass("hide");

    // Make the submit button appear
    $("#submit-fav-btn").removeClass("hide");
};

Favourites.cancel = () => {
    $("#edit-favs-btn").text("Edit").css("background-color", "");;

    // Restore the previous values
    $("fav-temp-input").val(State.favourites.temperature);
    $("fav-hum-input").val(State.favourites.humidity);
    $("fav-light-input").val(State.favourites.light_intensity);

    // Clear inputs and make them disappear
    $(".fav-input").addClass("hide");
    $(".fav-val").removeClass("hide");

    // Hide the submit button
    $("#submit-fav-btn").addClass("hide");
};

Favourites.updateArrows = async () => {
    // Temperature
    const tempDiff = Math.abs(State.favourites.temperature - State.sensors.temperature);
    const isTempLower = State.favourites.temperature > State.sensors.temperature;

    $("#fav-temp-svg")
        .attr("transform", isTempLower ? "rotate(180)" : "rotate(0)")
        .css("color", isTempLower ? "#C25B5B" : "#88FF88");

    if (tempDiff < TEMP_TRESHOLD) {
        $("#fav-temp-ok").show();
        $("#fav-temp-svg").hide();
    } else {
        $("#fav-temp-ok").hide();
        $("#fav-temp-svg").show();
    }

    // Humidity
    const humDiff = Math.abs(State.favourites.humidity - State.sensors.humidity);
    const isHumLower = State.favourites.humidity > State.sensors.humidity;

    $("#fav-hum-svg")
        .attr("transform", isHumLower ? "rotate(180)" : "rotate(0)")
        .css("color", isHumLower ? "#C25B5B" : "#88FF88");

    if (humDiff < HUM_TRESHOLD) {
        $("#fav-hum-ok").show();
        $("#fav-hum-svg").hide();
    } else {
        $("#fav-hum-ok").hide();
        $("#fav-hum-svg").show();
    }

    // Light
    const lightDiff = Math.abs(State.favourites.light_intensity - State.sensors.light_intensity);
    const isLightLower = State.favourites.light_intensity > State.sensors.light_intensity;

    $("#fav-light-svg")
        .attr("transform", isLightLower ? "rotate(180)" : "rotate(0)")
        .css("color", isLightLower ? "#C25B5B" : "#88FF88");

    if (lightDiff < LIGHT_TRESHOLD) {
        $("#fav-light-ok").show();
        $("#fav-light-svg").hide();
    } else {
        $("#fav-light-ok").hide();
        $("#fav-light-svg").show();
    }
}

Favourites.submit = async () => {
    const favTempInput = $("#fav-temp-input").val();
    const favHumInput = $("#fav-hum-input").val();
    const favLightInput = $("#fav-light-input").val();

    // If one of the fields are empty, don't allow it to go further
    if (favTempInput === "" || favHumInput === "" || favLightInput === "") return;

    const data = {
        temperature: parseFloat(favTempInput),
        humidity: parseFloat(favHumInput),
        light: parseInt(favLightInput),
    };

    // Disable button
    $("#submit-fav-btn").attr("disabled", true).addClass("disabled");

    // Send a request
    const res = await fetch("/set-favourites", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
    })

    if (res.status !== 200) return;

    // Now update the displayed fields
    StateFunctions.updateFavourites({
        temperature: data.temperature,
        humidity: data.humidity,
        light_intensity: data.light,
    })

    // Make the inputs disappear
    $("#edit-favs-btn").text("Edit").css("background-color", "");;
    $(".fav-input").addClass("hide");
    $(".fav-val").removeClass("hide");

    // Hide the submit button
    $("#submit-fav-btn").addClass("hide").removeClass("disabled").attr("disabled", false);
};

$(document).ready(async function () {
    $("#edit-favs-btn").click(() => {
        $("#edit-favs-btn").text() === "Edit" ? Favourites.edit() : Favourites.cancel();
    });

    $("#submit-fav-btn").click(() => {
        // Submit the form
        Favourites.submit();
    });
});