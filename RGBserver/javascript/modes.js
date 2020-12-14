const speed = document.getElementById("speed")
const standard = document.getElementById("standard")
const rainbow = document.getElementById("rainbow")
const norway = document.getElementById("norway")
const colorDrip = document.getElementById("colorDrip")
const alarmClock = document.getElementById("alarmClock")
const theaterChase = document.getElementById("theaterChase")
const sliderButtonModes = document.getElementById("phonebutton-slider-modes")

standard.setAttribute("href", `${url}/?panel=modes&mode=standard`)
rainbow.setAttribute("href", `${url}/?panel=modes&mode=rainbow`)
theaterChase.setAttribute("href", `${url}/?panel=modes&mode=theaterChase`)
norway.setAttribute("href", `${url}/?panel=modes&mode=norway`)
colorDrip.setAttribute("href", `${url}/?panel=modes&mode=colorDrip`)

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

sliderButtonModes.addEventListener("click", (event) => {
    window.location.replace(`${url}/?panel=modes&speed=${speed.value}`)
})

alarmClock.addEventListener("click", (event) => {
    const alarmTime = prompt("What time do you want to wake up?", "Insert value")
    window.location.replace(`${url}/?panel=modes&mode=alarmClock&alarmTime=${alarmTime}`)
})

speed.onmouseup = () => {
    window.location.replace(`${url}/?panel=modes&speed=${speed.value}`)
}
