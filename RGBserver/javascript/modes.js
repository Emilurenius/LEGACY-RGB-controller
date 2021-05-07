const speed = document.getElementById("speed")
const standard = document.getElementById("standard")
const rainbow = document.getElementById("rainbow")
const norway = document.getElementById("norway")
const colorDrip = document.getElementById("colorDrip")
const alarmClock = document.getElementById("alarmClock")
const theaterChase = document.getElementById("theaterChase")
const sliderButtonModes = document.getElementById("phonebutton-slider-modes")
const modeButtonsContainer = document.getElementById("animations&presets")


function loadModesButtons() {
    buttons = getJSON(`${url}/json/modeButtons.json`)
    console.log(buttons)

    modeButtonsContainer.innerHTML = ""
    for (const [k, v] of Object.entries(buttons.animations)) {
        const button = document.createElement("input")
        button.type = "button"
        button.classList.add("button")
        button.value = v.displayName
        button.id = k
    }
}loadModesButtons()

standard.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=standard`)
})

rainbow.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=rainbow`)
})

norway.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=norway`)
})

colorDrip.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=colorDrip`)
})

alarmClock.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=alarmClock`)
})

theaterChase.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=theaterChase`)
})

speed.value = getJSON(`${url}/json/data.json`).speed

sliderButtonModes.addEventListener("click", (event) => {
    getJSON(`${url}/?panel=modes&speed=${speed.value}`)
})

alarmClock.addEventListener("click", (event) => {
    const alarmTime = prompt("What time do you want to wake up?", `${getJSON(`${url}/json/data.json`).alarmClockData.alarmTime}`)
    console.log(event)

    if (alarmTime == null) {
        alert("Alarm Clock cancelled")
    }
    else {
        getJSON(`${url}/?panel=modes&mode=alarmClock&alarmTime=${alarmTime}`)
    }
})

speed.onchange = () => {
    getJSON(`${url}/?panel=modes&speed=${speed.value}`)
}