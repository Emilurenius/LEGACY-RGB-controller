const serverValueReadout = document.getElementById("serverValueReadout")
const serverValueReset = document.getElementById("serverValueReset")

serverValueReset.addEventListener("click", (evt) => {
    const serverState = getJSON(`${url}/json/data.json`)
    console.log(serverState)

    const toggleState = document.createElement("p")
    if (serverState.onoff == true) {
        const toggleStateValue = document.createTextNode("Lightstate: On")
    }
    else {
        const toggleStateValue = document.createTextNode("Lightstate: Off")
    }
    toggleState.appendChild(toggleStateValue)
    serverValueReadout.appendChild(toggleState)

    const r = document.createElement("p")
    r.appendChild(document.createTextNode(`Red: ${serverState.R}`))
    const g = document.createElement("p")
    g.appendChild(document.createTextNode(`Green: ${serverState.G}`))
    const b = document.createElement("p")
    b.appendChild(document.createTextNode(`Blue: ${serverState.B}`))
    const br = document.createElement("p")
    br.appendChild(document.createTextNode(` Brightness: ${serverState.brightness}`))

    serverValueReadout.appendChild(r)
    serverValueReadout.appendChild(g)
    serverValueReadout.appendChild(b)
    serverValueReadout.appendChild(br)
    serverValueReadout.appendChild(document.createElement("br"))

    const speed = document.createElement("p")
    speed.appendChild(document.createTextNode(`Animation speed: ${serverState.speed}`))
    const alarmClockTime = document.createElement("p")
    alarmClockTime.appendChild(docuemtn.createTextNode(`Alarm clock activation time: ${serverState.alarmClockData.alarmTime}`))

    serverValueReadout.appendChild(speed)
    serverValueReadout.appendChild(alarmClockTime)

})