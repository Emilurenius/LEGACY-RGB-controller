const speed                = document.getElementById("speed"             )
const standard             = document.getElementById("standard"          )
const modeButtonsContainer = document.getElementById("animations&presets")


function loadModesButtons() {
    buttons = getJSON(`${url}/json/modeButtons.json`)
    console.log(buttons)

    function buttonLoader(val) {
        for (const [k, v] of Object.entries(buttons[val])) {
            const button = document.createElement("input")
            button.type = "button"
            button.classList.add("button")
            button.value = v.displayName
            button.id = k
    
            button.onclick = (event) => {
                console.log(event.target.id)
                getJSON(`${url}/modes/set?mode=${event.target.id}`)
            }
    
            modeButtonsContainer.appendChild(button)
        }
    }

    modeButtonsContainer.innerHTML = ""
    modeButtonsContainer.appendChild(textFormat("Animations and presets", "Main-Text"))
    buttonLoader("animations") // Separated in code, so they can be more easily separated in functionality and in the control panel later. (If needed)
    buttonLoader("presets")
}loadModesButtons()

standard.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=standard`)
})



speed.value = getJSON(`${url}/json/data.json`).speed

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
    getJSON(`${url}/speed?speed=${speed.value}`)
    console.log(speed.value)
}