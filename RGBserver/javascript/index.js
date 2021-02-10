const url = (new URL(document.location)).origin
const brightness = document.getElementById("brightness")
const R = document.getElementById("R")
const G = document.getElementById("G")
const B = document.getElementById("B")
const sliderButtonMain = document.getElementById("phonebutton-slider-main")
const toggle = document.getElementById("toggle")


function getJSON(url) {
    var j = []
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) { j = data},
        async: false
    })
    return j
}

brightness.value = getJSON(`${url}/json/data.json`).brightness
R.value = getJSON(`${url}/json/data.json`).R
G.value = getJSON(`${url}/json/data.json`).G
B.value = getJSON(`${url}/json/data.json`).B

toggle.addEventListener("click", (event) => {
    const lightState = getJSON(`${url}/lightstate?toggle=change`)
    updateBackgroundColor()
    updateBackgroundLightState(lightState)
})

sliderButtonMain.addEventListener("click", (event) => {
    getJSON(`${url}/?panel=main&br=${brightness.value}&r=${R.value}&g=${G.value}&b=${B.value}`)
    updateBackgroundColor()
})

brightness.onmouseup = () => {
    getJSON(`${url}/?panel=main&br=${brightness.value}`)
    updateBackgroundColor()
}

R.onmouseup = () => {
    getJSON(`${url}/?panel=main&r=${R.value}`)
    updateBackgroundColor()
}

G.onmouseup = () => {
    getJSON(`${url}/?panel=main&g=${G.value}`)
    updateBackgroundColor()
}

B.onmouseup = () => {
    getJSON(`${url}/?panel=main&b=${B.value}`)
    updateBackgroundColor()
}

updateBackgroundLightState(getJSON(`${url}/lightstate`))
