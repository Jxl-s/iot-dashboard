const LED = {};

LED.setState = function (isOn) {
    const lightAddClass = isOn ? "on" : "off";
    const lightRemoveClass = isOn ? "off" : "on";
    const lightText = isOn ? "(ON)" : "(OFF)";

    const iconAddClass = isOn ? "light-icon-on" : "icon-off";
    const iconRemoveClass = isOn ? "icon-off" : "light-icon-on";

    const buttonAddClass = isOn ? "lg-button-on" : "lg-button-off";
    const buttonRemoveClass = isOn ? "lg-button-off" : "lg-button-on";
    const buttonText = isOn ? "Turn OFF" : "Turn ON";

    $("#light-indicator")
        .addClass(lightAddClass)
        .removeClass(lightRemoveClass)
        .text(lightText);

    $("#light-icon-indicator")
        .addClass(iconAddClass)
        .removeClass(iconRemoveClass)

    $("#light-toggle")
        .addClass(buttonAddClass)
        .removeClass(buttonRemoveClass)
        .text(buttonText);
}

$(document).ready(async function () {
    $("#light-toggle").click(async function () {
        // New status will be False if it's currently ON
        document._socket?.emit("set_light", !State.light);
    });
});