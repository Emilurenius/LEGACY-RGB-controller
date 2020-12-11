const speed = document.getElementById("speed")
const standard = document.getElementById("standard")
const rainbow = document.getElementById("rainbow")
const norway = document.getElementById("norway")
const colorDrip = document.getElementById("colorDrip")
const alarmClock = document.getElementById("alarmClock")
const back = document.getElementById("back")
const theaterChase = document.getElementById("theaterChase")
const sliderButton = document.getElementById("phonebutton-slider")

standard.setAttribute("href", `${url}/modes?panel=modes&mode=standard`)
rainbow.setAttribute("href", `${url}/modes?panel=modes&mode=rainbow`)
theaterChase.setAttribute("href", `${url}/modes?panel=modes&mode=theaterChase`)
norway.setAttribute("href", `${url}/modes?panel=modes&mode=norway`)
colorDrip.setAttribute("href", `${url}/modes?panel=modes&mode=colorDrip`)
back.setAttribute("href", `${url}/`)

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
    window.location.replace(`${url}/modes?panel=modes&speed=${speed.value}`)
})

alarmClock.addEventListener("click", (event) => {
    const alarmTime = prompt("What time do you want to wake up?", "Insert value")
    window.location.replace(`${url}/modes?panel=modes&mode=alarmClock&alarmTime=${alarmTime}`)
})

speed.onmouseup = () => {
    window.location.replace(`${url}/modes?panel=modes&speed=${speed.value}`)
}
