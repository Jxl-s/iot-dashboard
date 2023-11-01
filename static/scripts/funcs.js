function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function roundTwoDecimals(x) {
    return Math.round(x * 100) / 100;
}

function inverseLerp(val, min, max) {
    if (min === max) return 0;
    return (val - min) / (max - min);
}

function hideNotif() {
    $("#notif-container").addClass("hide");
}

function sendNotif(type, title, body) {
    $("#notif-title").text(title);
    $("#notif-body").text(body);
    $("#notif-container").removeClass("hide");

    // Set the color
    if (type === "error") {
        $("#notif-frame").css("background-color", "rgb(171, 100, 100)");
    } else if (type === "success") {
        $("#notif-frame").css("background-color", "rgb(100, 171, 100)");
    } else {
        $("#notif-frame").css("background-color", "");
    }

    // Hide after 2 seconds
    setTimeout(() => {
        $("#notif-container").addClass("hide");
    }, 2000);
}

$(document).ready(function () {
    const getTimeString = () => new Date().toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
    });

    const getDayString = () => new Date().toLocaleDateString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Update time loop
    const updateLabels = () => {
        $("#time-label").text(getTimeString());
        $("#day-label").text(getDayString());
    }

    updateLabels();
    setInterval(updateLabels, 1000);
});