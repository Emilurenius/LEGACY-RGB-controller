const savePresetButton = document.getElementById("savePreset")
const presetContainer = document.getElementById("presets")

savePresetButton.addEventListener("click", (event) => {
    console.log(R.value)
    console.log(G.value)
    console.log(B.value)
    const presetName = prompt("What do you want to call the preset?", "")

    getJSON(`${url}/presets?mode=new&presetName=${presetName}&R=${R.value}&G=${G.value}&B=${B.value}`)
})

function loadPresetButtons(JSONdataURL) {
    const JSONdata = getJSON(JSONdataURL)
    console.log(JSONdata)
    for (const [k, v] of Object.entries(JSONdata)) {
        const name = k
        const R = v.R
        const G = v.G
        const B = v.B
        console.log(`${name}: ${R} ${G} ${B}`)

        const averageBrightness = parseInt(R) + parseInt(G) + parseInt(B) / 3
        console.log(averageBrightness)
        let textColor = null
        if (averageBrightness < 128) {
            textColor = "white"
        }
        else {
            textColor = "black"
        }

        const button = document.createElement("input")
        button.type = "button"
        button.classList.add("button")
        button.value = name

        button.onclick = (event) => {
            console.log(event.name)
            //updateRGB(R, G, B)
        }

        button.style = `background: rgb(${R}, ${G}, ${B}); color: ${textColor};`
        presetContainer.appendChild(button)
    }
}

function updateRGB(R, G, B) {
    getJSON(`${url}/rgb?R=${R}&G=${G}&B=${B}`)
    updateBackgroundLightState(getJSON(`${url}/lightstate`))
}

loadPresetButtons(`${url}/presets?mode=load`)