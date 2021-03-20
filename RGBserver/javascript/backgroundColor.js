function updateBackgroundColor() {
    document.body.style.backgroundColor = `rgb(${R.value}, ${G.value}, ${B.value})`
}

function updateBackgroundLightState(lightState) {
    if (lightState == true) {
        const red = R.value * (brightness.value / 1000)
        const green = G.value * (brightness.value / 1000)
        const blue = B.value * (brightness.value / 1000)

        document.body.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`
    }
    else {
        document.body.style.backgroundColor = `rgb(0, 0, 0)`
    }
}