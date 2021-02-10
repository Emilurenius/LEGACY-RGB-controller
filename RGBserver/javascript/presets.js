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
    for (let i = 0; i < JSONdata.length; i ++) {
        const name = JSONdata[i]
        const R = JSONddata[i].R
        const G = JSONddata[i].G
        const B = JSONddata[i].B

        const button = document.createElement("input")
        button.type = "button"
        button.classList.add("button")
        console.log("Hello world")
        console.log(JSONdata[i])
    }
}

loadPresetButtons(`${url}/presets?mode=load`)