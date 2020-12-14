const serverReadout = document.getElementById("serverReadout")
const serverValueReset = document.getElementById("serverValueReset")

function updateServerState() {
    serverReadout.innerHTML = ""
    const serverState = getJSON(`${url}/json/data.json`)
    console.log(serverState)

    const toggleState = document.createElement("p")
    let toggleStateValue = undefined
    if (serverState.onoff == true) {
        toggleStateValue = document.createTextNode("Lightstate: On")
    }
    else {
        toggleStateValue = document.createTextNode("Lightstate: Off")
    }
    toggleState.appendChild(toggleStateValue)
    serverReadout.appendChild(toggleState)

    const r = document.createElement("p")
    r.appendChild(document.createTextNode(`Red: ${serverState.R}`))
    const g = document.createElement("p")
    g.appendChild(document.createTextNode(`Green: ${serverState.G}`))
    const b = document.createElement("p")
    b.appendChild(document.createTextNode(`Blue: ${serverState.B}`))
    const br = document.createElement("p")
    br.appendChild(document.createTextNode(` Brightness: ${serverState.brightness}%`))

    serverReadout.appendChild(r)
    serverReadout.appendChild(g)
    serverReadout.appendChild(b)
    serverReadout.appendChild(br)
    serverReadout.appendChild(document.createElement("br"))

    const speed = document.createElement("p")
    speed.appendChild(document.createTextNode(`Animation speed: ${serverState.speed}`))
    const mode = document.createElement("p")
    mode.appendChild(document.createTextNode(`Current mode: ${serverState.mode}`))
    const alarmClockTime = document.createElement("p")
    alarmClockTime.appendChild(document.createTextNode(`Alarm clock activation time: ${serverState.alarmClockData.alarmTime}`))

    serverReadout.appendChild(speed)
    serverReadout.appendChild(mode)
    serverReadout.appendChild(alarmClockTime)
}

serverValueReset.addEventListener("click", (evt) => {
    updateServerState()
})

updateServerState()