const Fan = {};

Fan.setState = function (isOn) {
    const fanAddClass = isOn ? "on" : "off";
    const fanRemoveClass = isOn ? "off" : "on";
    const fanText = isOn ? "(ON)" : "(OFF)";

    const iconAddClass = isOn ? "fan-icon-on" : "icon-off";
    const iconRemoveClass = isOn ? "icon-off" : "fan-icon-on";

    const buttonAddClass = isOn ? "lg-button-on" : "lg-button-off";
    const buttonRemoveClass = isOn ? "lg-button-off" : "lg-button-on";
    const buttonText = isOn ? "Turn OFF" : "Turn ON";

    $("#fan-indicator")
        .addClass(fanAddClass)
        .removeClass(fanRemoveClass)
        .text(fanText);

    $("#fan-icon-indicator")
        .addClass(iconAddClass)
        .removeClass(iconRemoveClass)

    $("#fan-toggle")
        .addClass(buttonAddClass)
        .removeClass(buttonRemoveClass)
        .text(buttonText);
}

$(document).ready(function () {
    $("#fan-toggle").click(() => {
        document._socket?.emit("set_fan", !State.fan)
    });
});