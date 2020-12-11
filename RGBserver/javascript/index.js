const url = (new URL(document.location)).origin
const brightness = document.getElementById("brightness")
const R = document.getElementById("R")
const G = document.getElementById("G")
const B = document.getElementById("B")
const sliderButtonMain = document.getElementById("phonebutton-slider-main")
const toggle = document.getElementById("toggle")
const modes = document.getElementById("modes")

toggle.setAttribute("href", `${url}/?panel=main&toggle=change`)
modes.setAttribute("href", `${url}/modes`)


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
    


sliderButtonMain.addEventListener("click", (event) => {
    window.location.replace(`${url}/?panel=main&br=${brightness.value}&r=${R.value}&g=${G.value}&b=${B.value}`)
})

brightness.onmouseup = () => {
    window.location.replace(`${url}/?panel=main&br=${brightness.value}`)
}

R.onmouseup = () => {
    window.location.replace(`${url}/?panel=main&r=${R.value}`)
}

G.onmouseup = () => {
    window.location.replace(`${url}/?panel=main&g=${G.value}`)
}

B.onmouseup = () => {
    window.location.replace(`${url}/?panel=main&b=${B.value}`)
}














