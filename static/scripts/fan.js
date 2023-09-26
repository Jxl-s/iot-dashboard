const FAN = {};

FAN.setOn = async function () {
    const res = await fetch("/set-fan/1", {
        method: "POST"
    });
    if (res.status != 200) return;

    // Text indicator
    $("#fan-indicator")
        .addClass("on")
        .removeClass("off")
        .text("(ON)");

    // Icon indicator
    $("#fan-icon-indicator")
        .addClass("fan-icon-on")
        .removeClass("icon-off")

    // Button
    $("#fan-toggle")
        .addClass("lg-button-on")
        .removeClass("lg-button-off")
        .text("Turn OFF");
}

FAN.setOff = async function () {
    const res = await fetch("/set-fan/0", {
        method: "POST"
    });
    if (res.status != 200) return;

    // Text indicator
    $("#fan-indicator")
        .removeClass("on")
        .addClass("off")
        .text("(OFF)");

    // Icon indicator
    $("#fan-icon-indicator")
        .removeClass("fan-icon-on")
        .addClass("icon-off")

    // Button
    $("#fan-toggle")
        .removeClass("lg-button-on")
        .addClass("lg-button-off")
        .text("Turn ON");
};

$(document).ready(async function () {
    $("#fan-toggle").click(async function () {
        // Different action depending on the current state
        $("#fan-indicator").text() == "(ON)" ? FAN.setOff() : FAN.setOn();
    });
});