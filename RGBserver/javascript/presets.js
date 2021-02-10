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

        const button = document.createElement("input")
        button.type = "button"
        button.classList.add("button")
        console.log("Hello world")
    }
}

loadPresetButtons(`${url}/presets?mode=load`)