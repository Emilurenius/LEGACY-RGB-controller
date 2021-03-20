function updateBackgroundColor() {
    document.body.style.backgroundColor = `rgb(${R.value}, ${G.value}, ${B.value})`
}

function updateBackgroundLightState(lightState) {
    if (lightState == true) {
        const R = R.value * (brightness.value / 1000)
        const G = G.value * (brightness.value / 1000)
        const B = B.value * (brightness.value / 1000)

        document.body.style.backgroundColor = `rgb(${R}, ${G}, ${B})`
    }
    else {
        document.body.style.backgroundColor = `rgb(0, 0, 0)`
    }
}