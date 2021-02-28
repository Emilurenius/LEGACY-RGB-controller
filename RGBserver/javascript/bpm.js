const bpmPresetContainer = document.getElementById("BPMpresets")
const bpmSlider = document.getElementById("BPMslider")
const bpmLabel = document.getElementById("BPMsliderLabel")
const bpmActivate = document.getElementById("activateBPMmode")
const bpmData = getJSON(`${url}/bpm?mode=getBPM`)

bpmSlider.value = bpmData.value
bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`

bpmSlider.onmouseup = () => {
    getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
    bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
}

bpmActivate.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=bpm`)
})