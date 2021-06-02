const brightness = document.getElementById("brightness")
const R = document.getElementById("R")
const G = document.getElementById("G")
const B = document.getElementById("B")
const sliderButtonMain = document.getElementById("phonebutton-slider-main")
const toggle = document.getElementById("toggle")

brightness.value = getJSON(`${url}/json/data.json`).brightness
R.value = getJSON(`${url}/json/data.json`).R
G.value = getJSON(`${url}/json/data.json`).G
B.value = getJSON(`${url}/json/data.json`).B

toggle.addEventListener("click", (event) => {
    updateBackgroundLightState(getJSON(`${url}/lightstate?toggle=change`))
})

brightness.onchange = () => {
    getJSON(`${url}/rgb?br=${brightness.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

R.onchange = () => {
    getJSON(`${url}/rgb?r=${R.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

G.onchange = () => {
    getJSON(`${url}/rgb?g=${G.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

B.onchange = () => {
    getJSON(`${url}/rgb?b=${B.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

updateBackgroundLightState(getJSON(`${url}/lightstate`))