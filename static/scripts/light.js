const LED = {};

LED.setOn = function () {
    // Text indicator
    $("#light-indicator")
        .addClass("on")
        .removeClass("off")
        .text("(ON)");

    // Icon indicator
    $("#light-icon-indicator")
        .addClass("light-icon-on")
        .removeClass("icon-off")

    // Button
    $("#light-toggle")
        .addClass("lg-button-on")
        .removeClass("lg-button-off")
        .text("Turn OFF");
}

LED.setOff = function () {
    // Text indicator
    $("#light-indicator")
        .removeClass("on")
        .addClass("off")
        .text("(OFF)");

    // Icon indicator
    $("#light-icon-indicator")
        .removeClass("light-icon-on")
        .addClass("icon-off")

    // Button
    $("#light-toggle")
        .removeClass("lg-button-on")
        .addClass("lg-button-off")
        .text("Turn ON");
};

$(document).ready(async function () {
    $("#light-toggle").click(async function () {
        // New status will be False if it's currently ON
        document._socket?.emit("set_light", !State.light);
    });
});