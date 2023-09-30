const Fan = {};

Fan.setOn = async function () {
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

Fan.setOff = async function () {
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

$(document).ready(function () {
    $("#fan-toggle").click(() => {
        document._socket?.emit("set_fan", !State.fan)
    });
});