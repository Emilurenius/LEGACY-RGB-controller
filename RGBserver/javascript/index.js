const url = (new URL(document.location)).origin
const brightness = document.getElementById("brightness")
const R = document.getElementById("R")
const G = document.getElementById("G")
const B = document.getElementById("B")
const sliderButton = document.getElementById("phonebutton-slider")
const toggle = document.getElementById("toggle")
const modes = document.getElementById("modes")

toggle.setAttribute("href", `${url}/?toggle=change`)
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
    


sliderButton.addEventListener("click", (event) => {
    window.location.replace(`${url}/?br=${brightness.value}&r=${R.value}&g=${G.value}&b=${B.value}`)
})

brightness.onmouseup = () => {
    window.location.replace(`${url}/?br=${brightness.value}`)
}

R.onmouseup = () => {
    window.location.replace(`${url}/?r=${R.value}`)
}

G.onmouseup = () => {
    window.location.replace(`${url}/?g=${G.value}`)
}

B.onmouseup = () => {
    window.location.replace(`${url}/?b=${B.value}`)
}














