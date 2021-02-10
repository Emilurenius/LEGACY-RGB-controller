function updateBackgroundColor() {
    document.body.style.backgroundColor = `rgb(${R.value}, ${G.value}, ${B.value})`
}

function updateBackgroundLightState(lightState) {
    if (lightState == true) {
        document.body.style.backgroundColor = `rgb(${R.value}, ${G.value}, ${B.value})`
    }
    else {
        document.body.style.backgroundColor = `rgb(0, 0, 0)`
    }
}