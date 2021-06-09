function bpmSettings() {
    const bpmPresetContainer = document.getElementById("BPMpresets")
    const bpmSlider = document.getElementById("BPMslider")
    const bpmLabel = document.getElementById("BPMsliderLabel")
    const spotifySyncButton = document.getElementById("spotifySyncButton")
    const bpmData = getJSON(`${url}/bpm?mode=getBPM`)

    bpmSlider.value = bpmData.value
    bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`

    spotifySyncButton.onclick = (event) => {
        const songData = getJSON("http://192.168.1.124:8000/getBPM")
        console.log(songData)
    }

    bpmSlider.onchange = () => {
        getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
        bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
    }
}
bpmSettings()