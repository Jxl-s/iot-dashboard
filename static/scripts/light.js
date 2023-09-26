const LED = {};

LED.setOn = async function () {
    const res = await fetch("/set-light/1", {
        method: "POST"
    });
    if (res.status != 200) return;

    // Text indicator
    $("#light-indicator")
        .addClass("on")
        .removeClass("off")
        .text("(ON)");

    // Icon indicator
    $("#light-icon-indicator")
        .addClass("icon-on")
        .removeClass("icon-off")

    // Button
    $("#light-toggle")
        .addClass("lg-button-on")
        .removeClass("lg-button-off")
        .text("Turn OFF");
}

LED.setOff = async function () {
    const res = await fetch("/set-light/0", {
        method: "POST"
    });
    if (res.status != 200) return;

    // Text indicator
    $("#light-indicator")
        .removeClass("on")
        .addClass("off")
        .text("(OFF)");

    // Icon indicator
    $("#light-icon-indicator")
        .removeClass("icon-on")
        .addClass("icon-off")

    // Button
    $("#light-toggle")
        .removeClass("lg-button-on")
        .addClass("lg-button-off")
        .text("Turn ON");
};

$(document).ready(async function () {
    $("#light-toggle").click(async function () {
        // Different action depending on the current state
        $("#light-indicator").text() == "(ON)" ? LED.setOff() : LED.setOn();
    });
});