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
R.value = getJSON(`${url}/json/data.json`)
G.value = getJSON(`${url}/json/data.json`)
B.value = getJSON(`${url}/json/data.json`)

toggle.addEventListener("click", (event) => {
    getJSON(`${url}/lightstate?toggle=change`)
})

sliderButtonMain.addEventListener("click", (event) => {
    getJSON(`${url}/?panel=main&br=${brightness.value}&r=${R.value}&g=${G.value}&b=${B.value}`)
})

brightness.onmouseup = () => {
    getJSON(`${url}/?panel=main&br=${brightness.value}`)
}

R.onmouseup = () => {
    getJSON(`${url}/?panel=main&r=${R.value}`)
}

G.onmouseup = () => {
    getJSON(`${url}/?panel=main&g=${G.value}`)
}

B.onmouseup = () => {
    getJSON(`${url}/?panel=main&b=${B.value}`)
}