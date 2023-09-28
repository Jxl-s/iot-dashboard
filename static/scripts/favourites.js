function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function roundTwoDecimals(x) {
    return Math.round(x * 100) / 100;
}

const Favourites = {};

const previousValues = {};
Favourites.edit = () => {
    $("#edit-favs-btn").text("Cancel").css("background-color", "#C25B5B");

    // Set the values before modifying
    $(".fav-input").each((index, element) => {
        previousValues[element.id] = element.value;
    });

    // And make the values disappear
    $(".fav-val").addClass("hide");
    $(".fav-input").removeClass("hide");

    // Make the submit button appear
    $("#submit-fav-btn").removeClass("hide");
};

Favourites.cancel = () => {
    $("#edit-favs-btn").text("Edit").css("background-color", "");;

    // Restore the previous values
    $(".fav-input").each((index, element) => {
        element.value = previousValues[element.id];
    });

    // Clear inputs and make them disappear
    $(".fav-input").addClass("hide");
    $(".fav-val").removeClass("hide");

    // Hide the submit button
    $("#submit-fav-btn").addClass("hide");
};

Favourites.updateArrows = async () => {
    const data = {
        temperature: previousValues["fav-temp-input"],
        humidity: previousValues["fav-hum-input"],
        light: previousValues["fav-light-input"],
    };

    // Compare to find the arrows
    const tempVal = parseFloat($("#sensor-temp-val").attr("iot-val"));
    const humVal = parseFloat($("#sensor-hum-val").attr("iot-val"));
    const lightVal = parseFloat($("#sensor-light-val").attr("iot-val"));

    // Temperature
    const newTempTransform = data.temperature < tempVal ? "rotate(180)" : "rotate(0)";
    const newTempColor = data.temperature < tempVal ? "#C25B5B" : "#88FF88";
    $("#fav-temp-svg").attr("transform", newTempTransform).css("color", newTempColor);

    // Humidity
    const newHumTransform = data.humidity < humVal ? "rotate(180)" : "rotate(0)";
    const newHumColor = data.humidity < humVal ? "#C25B5B" : "#88FF88";
    $("#fav-hum-svg").attr("transform", newHumTransform).css("color", newHumColor);

    // Light
    const newLightTransform = data.light < lightVal ? "rotate(180)" : "rotate(0)";
    const newLightColor = data.light < lightVal ? "#C25B5B" : "#88FF88";
    $("#fav-light-svg").attr("transform", newLightTransform).css("color", newLightColor);
    
    console.log("Hi");
}

Favourites.submit = async () => {
    // If one of the fields are empty, don't allow it to go further
    if ($("#fav-temp-input").val() === "") return;
    if ($("#fav-hum-input").val() === "") return;
    if ($("#fav-light-input").val() === "") return;

    const data = {
        temperature: parseFloat($("#fav-temp-input").val()),
        humidity: parseFloat($("#fav-hum-input").val()),
        light: parseInt($("#fav-light-input").val()),
    };

    $("#submit-fav-btn").attr("disabled", true).addClass("disabled");

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
    $("#fav-temp-val").text(`${roundTwoDecimals(data.temperature)}°C`);
    $("#fav-hum-val").text(`${roundTwoDecimals(data.humidity)}%`);
    $("#fav-light-val").text(`${numberWithCommas(data.light)} lux`);

    $(".fav-input").each((index, element) => {
        previousValues[element.id] = element.value;
    });

    Favourites.updateArrows();

    // Make the inputs disappear
    $("#edit-favs-btn").text("Edit").css("background-color", "");;
    $(".fav-input").addClass("hide");
    $(".fav-val").removeClass("hide");

    // Hide the submit button
    $("#submit-fav-btn").addClass("hide").removeClass("disabled").attr("disabled", false);
};

$(document).ready(async function () {
    // Initally set the values
    $(".fav-input").each((index, element) => {
        previousValues[element.id] = element.value;
    });

    $("#edit-favs-btn").click(() => {
        $("#edit-favs-btn").text() === "Edit" ? Favourites.edit() : Favourites.cancel();
    });

    $("#submit-fav-btn").click(() => {
        // Submit the form
        Favourites.submit();
    });
});