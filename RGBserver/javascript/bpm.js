const bpmPresetContainer = document.getElementById("BPMpresets")
const bpmSlider = document.getElementById("BPMslider")
const bpmLabel = document.getElementById("BPMsliderLabel")
const bpmSliderButton = document.getElementById("phonebutton-slider-bpm")
const spotifySyncButton = document.getElementById("spotifySyncButton")
const bpmData = getJSON(`${url}/bpm?mode=getBPM`)

bpmSlider.value = bpmData.value
bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
spotifySyncButton.href = `http://192.168.1.124:8000/getBPM`

bpmSlider.onchange = () => {
    getJSON(`${url}/bpm?mode=updateBPM&bpm=${bpmSlider.value}`)
    bpmLabel.innerHTML = `BPM: ${bpmSlider.value}`
}

if (window.Worker && queries.bpmLiveUpdate == "true") {
    if (queries.newSongID != undefined) {
        if (queries.currentSong != queries.songID) {
            window.location.replace("http://192.168.1.124:8000/getBPM")
        }
    }
    console.log("Worker compatible")
    const myWorker = new Worker(`${url}/javascript/workers/bpmWorker.js`)
    const message = {nextSongAt: queries.songEnd}

    myWorker.postMessage(message)

    myWorker.onmessage = (e) => {
        console.log(e.data.response)
        if (e.data.response == "song done") {
            window.location.replace("http://192.168.1.124:8000/getBPM")
        }
        else if (e.data.response == "checkSong") {
            window.location.replace("http://192.168.1.124:8000/getCurrentTrack")
        }
    }
}