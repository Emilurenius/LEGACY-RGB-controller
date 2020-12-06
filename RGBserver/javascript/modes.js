const url = (new URL(document.location)).origin
const speed = document.getElementById("speed")
const standard = document.getElementById("standard")
const rainbow = document.getElementById("rainbow")
const sliderButton = document.getElementById("phonebutton-slider")

standard.setAttribute("href", `${url}/modes?mode=standard`)
rainbow.setAttribute("href", `${url}/modes?mode=rainbow`)

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

speed.value = getJSON(`${url}/json/data.json`).speed

sliderButton.addEventListener("click", (event) => {
    window.location.replace(`${url}/modes?speed=${speed.value}`)
})


speed.onmouseup = () => {
    window.location.replace(`${url}/modes?speed=${speed.value}`)
}
