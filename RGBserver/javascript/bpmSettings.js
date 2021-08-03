function bpmSettings() {
    const spotifySync = document.getElementById("spotifySyncButton")
    const bpmSlider = document.getElementById("BPMslider")
    const bpmSliderLabel = document.getElementById("BPMsliderLabel")
    bpmData = getJSON(`${url}/json/bpm.json`)
    console.log(bpmData)

    function syncSlider() {
        bpmSlider.value = bpmData.value
        bpmSliderLabel.innerHTML = `BPM: ${bpmData.value}`
    }
    syncSlider()

    bpmSlider.onchange = () => {
        getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
        syncSlider()
    }

    spotifySync.addEventListener("click", (event) => {

        res = getJSON(`${url}/spotify/getBPM`)
        console.log(res)
        if (res.length == 0) {
            alert("No song data recieved! Attempting login")
            window.location.replace(`${url}/spotify/login`)
        }
        syncSlider()
    })
}
bpmSettings()