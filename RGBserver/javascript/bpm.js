const bpmPresetContainer = document.getElementById("BPMpresets")
const bpmSlider = document.getElementById("BPMslider")
const bpmLabel = document.getElementById("BPMsliderLabel")
const bpmSliderButton = document.getElementById("phonebutton-slider-bpm")
const bpmActivate = document.getElementById("activateBPMmode")
const spotifySyncButton = document.getElementById("spotifySyncButton")
const bpmData = getJSON(`${url}/bpm?mode=getBPM`)

bpmSlider.value = bpmData.value
bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
spotifySyncButton.href = `http://192.168.1.124:8000/getBPM`

bpmSlider.onmouseup = () => {
    getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
    bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
}

bpmActivate.addEventListener("click", (event) => {
    getJSON(`${url}/modes/set?mode=bpm`)
})

bpmSliderButton.addEventListener("click", (event) => {
    getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
    bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
})