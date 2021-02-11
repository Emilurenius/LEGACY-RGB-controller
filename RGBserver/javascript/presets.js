const savePresetButton = document.getElementById("savePreset")
const presetContainer = document.getElementById("presets")

savePresetButton.addEventListener("click", (event) => {
    console.log(R.value)
    console.log(G.value)
    console.log(B.value)
    const presetName = prompt("What do you want to call the preset?", "")

    getJSON(`${url}/presets?mode=new&presetName=${presetName}&R=${R.value}&G=${G.value}&B=${B.value}`)
    loadPresetButtons()
})

function loadPresetButtons() {
    const JSONdata = getJSON(`${url}/presets?mode=load`)
    presetContainer.innerHTML = ""
    for (const [k, v] of Object.entries(JSONdata)) {
        const name = k
        const R = v.R
        const G = v.G
        const B = v.B

        const averageBrightness = parseInt(R) + parseInt(G) + parseInt(B) / 3
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
        button.id = name

        button.onclick = (event) => {
            console.log(event.target.id)
            
            const JSONdata = getJSON(`${url}/presets?mode=load`)
            for (const [k, v] of Object.entries(JSONdata)) {
                if (k == event.target.id) {
                    console.log("match found")
                    console.log(`${url}/rgb?r=${v.R}&g=${v.G}&b=${v.B}`)
                    getJSON(`${url}/rgb?r=${v.R}&g=${v.G}&b=${v.B}`)

                    document.getElementById("R").value = v.R
                    document.getElementById("G").value = v.G
                    document.getElementById("B").value = v.B

                    updateBackgroundLightState(getJSON(`${url}/lightstate`))
                }
            }
        }

        button.style = `background: rgb(${R}, ${G}, ${B}); color: ${textColor};`
        presetContainer.appendChild(button)
    }
}

function updateRGB(R, G, B) {
    getJSON(`${url}/rgb?R=${R}&G=${G}&B=${B}`)
    updateBackgroundLightState(getJSON(`${url}/lightstate`))
}

loadPresetButtons()