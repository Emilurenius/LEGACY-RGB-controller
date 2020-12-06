const url = (new URL(document.location)).origin
const bSpeed = document.getElementById("bSpeed")
const sliderButton = document.getElementById("phonebutton-slider")

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

bSpeed.value = getJSON(`${url}/json/data.json`).breatheSpeed

sliderButton.addEventListener("click", (event) => {
    window.location.replace(`${url}/modes?bSpeed=${bSpeed.value}`)
})


bSpeed.onmouseup = () => {
    window.location.replace(`${url}/modes?bSpeed=${bSpeed.value}`)
}
