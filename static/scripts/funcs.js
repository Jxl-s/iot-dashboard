function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function roundTwoDecimals(x) {
    return Math.round(x * 100) / 100;
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