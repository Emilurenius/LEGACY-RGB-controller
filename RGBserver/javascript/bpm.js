const bpmPresetContainer = document.getElementById("BPMpresets")
const bpmSlider = document.getElementById("BPMslider")
const bpmLabel = document.getElementById("BPMsliderlabel")
const bpmData = getJSON(`${url}/bpm?mode=getBPM`)

bpmSlider.value = bpmData.value
bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`

bpmSlider.onmouseup = () => {
    getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
}