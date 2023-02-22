function colorBubblesSettings() {
    const tLengthSlider = document.getElementById("tLengthSlider")
    const bDistSlider = document.getElementById("bDistSlider")
    const tLengthSliderLabel = document.getElementById("tLengthSliderLabel")
    const bDistSliderLabel = document.getElementById("bDistSliderLabel")

    function syncSlider(onlyLabel=false) {
        const sliderVals = getJSON(`${url}/json/colorBubblesSettings.json`)
        if (!onlyLabel) {
            tLengthSlider.value = sliderVals.tailLength
            bDistSlider.value = sliderVals.bubbleDistance
        }
        tLengthSliderLabel.innerHTML = `Tail Length: ${sliderVals.tailLength}`
        bDistSliderLabel.innerHTML = `Bubble Distance: ${sliderVals.bubbleDistance}`
    }
    syncSlider()

    tLengthSlider.onchange = () => {
        getJSON(`${url}/settings/colorBubbles?tLength=${tLengthSlider.value}`)
        syncSlider(onlyLabel=true)
    }
    bDistSlider.onchange = () => {
        getJSON(`${url}/settings/colorBubbles?bDist=${bDistSlider.value}`)
        syncSlider(onlyLabel=true)
    }
}
colorBubblesSettings()