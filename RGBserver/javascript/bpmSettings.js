function bpmSettings() {
    const spotifySync = document.getElementById("spotifySyncButton")
    const bpmSlider = document.getElementById("BPMslider")
    const bpmSliderLabel = document.getElementById("BPMsliderLabel")
    const BPManimationType = document.getElementById("BPManimationType")
    bpmData = getJSON(`${url}/json/bpm.json`)
    console.log(bpmData)

    function syncSlider(onlyLabel=false) {
        bpmData = getJSON(`${url}/json/bpm.json`)
        if (!onlyLabel) {
            bpmSlider.value = bpmData.value
        }
        console.log(bpmSlider.value)
        bpmSliderLabel.innerHTML = `BPM: ${bpmData.value}`
    }
    syncSlider()

    bpmSlider.onchange = () => {
        getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
        syncSlider(onlyLabel=true)
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

    BPManimationType.addEventListener("change", (event) => {
        getJSON(`${url}/settings/bpm?animationType=${BPManimationType.options[BPManimationType.selectedIndex].value}`)
    })
}
bpmSettings()