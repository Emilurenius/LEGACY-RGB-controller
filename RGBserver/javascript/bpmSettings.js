function bpmSettings() {
    const spotifySync = document.getElementById("spotifySyncButton")
    const bpmSlider = document.getElementById("BPMslider")
    const bpmSliderLabel = document.getElementById("BPMsliderLabel")
    bpmData = getJSON(`${url}/json/bpm.json`)
    console.log(bpmData)

    bpmSliderLabel.innerHTML = `BPM: ${bpmData.value}`

    bpmSlider.onchange = () => {
        bpmSliderLabel.innerHTML = `BPM: ${bpmSlider.value}`
        getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
    }

    spotifySync.addEventListener("click", (event) => {
        console.log("spotifySync")

        res = getJSON(`${url}/spotify/getBPM`)
        console.log(url)
        if (res.length == 0) {
            alert("No song data recieved! Attempting login")
            window.location.replace(`${url}/spotify/login`)
        }
    })
}
bpmSettings()