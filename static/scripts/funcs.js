function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function roundTwoDecimals(x) {
    return Math.round(x * 100) / 100;
}
