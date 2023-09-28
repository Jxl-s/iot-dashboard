function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function roundTwoDecimals(x) {
    return Math.round(x * 100) / 100;
}

const Favourites = {};

const previousValues = {};
Favourites.edit = () => {
    $("#edit-favourites-button").text("Cancel").css("background-color", "#C25B5B");

    // Get the values before modifying
    $(".favourites-input").each((index, element) => {
        previousValues[element.id] = element.value;
    });

    // And make the values disappear
    $(".favourites-value").addClass("hide");
    $(".favourites-input").removeClass("hide");

    // Make the submit button appear
    $("#submit-favourites-button").removeClass("hide");
};

Favourites.cancel = () => {
    $("#edit-favourites-button").text("Edit").css("background-color", "");;

    // Restore the previous values
    $(".favourites-input").each((index, element) => {
        element.value = previousValues[element.id];
    });

    // Clear inputs and make them disappear
    $(".favourites-input").addClass("hide");
    $(".favourites-value").removeClass("hide");

    // Hide the submit button
    $("#submit-favourites-button").addClass("hide");
};

Favourites.updateArrows = async () => {
    const data = {
        temperature: previousValues["favourite-temperature-input"],
        humidity: previousValues["favourite-humidity-input"],
        light: previousValues["favourite-light-input"],
    };

    // Compare to find the arrows
    const tempVal = parseFloat($("#sensor-temp-val").attr("iot-val"));
    const humVal = parseFloat($("#sensor-hum-val").attr("iot-val"));
    const lightVal = parseFloat($("#sensor-light-val").attr("iot-val"));

    // Temperature
    const newTempTransform = data.temperature < tempVal ? "rotate(180)" : "rotate(0)";
    const newTempColor = data.temperature < tempVal ? "#C25B5B" : "#88FF88";
    $("#favourite-temperature-svg").attr("transform", newTempTransform).css("color", newTempColor);

    // Humidity
    const newHumTransform = data.humidity < humVal ? "rotate(180)" : "rotate(0)";
    const newHumColor = data.humidity < humVal ? "#C25B5B" : "#88FF88";
    $("#favourite-humidity-svg").attr("transform", newHumTransform).css("color", newHumColor);

    // Light
    const newLightTransform = data.light < lightVal ? "rotate(180)" : "rotate(0)";
    const newLightColor = data.light < lightVal ? "#C25B5B" : "#88FF88";
    $("#favourite-light-svg").attr("transform", newLightTransform).css("color", newLightColor);
}

Favourites.submit = async () => {
    // If one of the fields are empty, don't allow it to go further
    if ($("#favourite-temperature-input").val() === "") return;
    if ($("#favourite-humidity-input").val() === "") return;
    if ($("#favourite-light-input").val() === "") return;

    const data = {
        temperature: parseFloat($("#favourite-temperature-input").val()),
        humidity: parseFloat($("#favourite-humidity-input").val()),
        light: parseInt($("#favourite-light-input").val()),
    };

    $("#submit-favourites-button").attr("disabled", true).addClass("disabled");

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
    $("#favourite-temperature-value").text(`${roundTwoDecimals(data.temperature)}°C`);
    $("#favourite-humidity-value").text(`${roundTwoDecimals(data.humidity)}%`);
    $("#favourite-light-value").text(`${numberWithCommas(data.light)} lux`);

    $(".favourites-input").each((index, element) => {
        previousValues[element.id] = element.value;
    });

    Favourites.updateArrows();

    // Make the inputs disappear
    $("#edit-favourites-button").text("Edit").css("background-color", "");;
    $(".favourites-input").addClass("hide");
    $(".favourites-value").removeClass("hide");

    // Hide the submit button
    $("#submit-favourites-button").addClass("hide").removeClass("disabled").attr("disabled", false);
};

$(document).ready(async function () {
    $("#edit-favourites-button").click(() => {
        $("#edit-favourites-button").text() === "Edit" ? Favourites.edit() : Favourites.cancel();
    });

    $("#submit-favourites-button").click(() => {
        // Submit the form
        Favourites.submit();
    });
});