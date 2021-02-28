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
    updateBackgroundLightState(getJSON(`${url}/lightstate?toggle=change`))
})

sliderButtonMain.addEventListener("click", (event) => {
    getJSON(`${url}/rgb?br=${brightness.value}&r=${R.value}&g=${G.value}&b=${B.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
})

brightness.onmouseup = () => {
    getJSON(`${url}/rgb?br=${brightness.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

R.onmouseup = () => {
    getJSON(`${url}/rgb?r=${R.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

G.onmouseup = () => {
    getJSON(`${url}/rgb?g=${G.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

B.onmouseup = () => {
    getJSON(`${url}/rgb?b=${B.value}`)
    updateBackgroundLightState(getJSON(`${url}/checklightstate`))
}

updateBackgroundLightState(getJSON(`${url}/lightstate`))