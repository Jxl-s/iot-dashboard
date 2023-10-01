function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function roundTwoDecimals(x) {
    return Math.round(x * 100) / 100;
}

function getTimeString() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function getDayString() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date().toLocaleDateString(undefined, options);
}

$(document).ready(function () {
    // Update time loop
    const updateLabels = () => {
        $("#time-label").text(getTimeString());
        $("#day-label").text(getDayString());
    }

    updateLabels();
    setInterval(updateLabels, 200);
});