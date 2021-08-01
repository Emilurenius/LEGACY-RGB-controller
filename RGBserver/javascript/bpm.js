function bpm() {
    const bpmActivate = document.getElementById("activateBPMmode")
    
    bpmActivate.addEventListener("click", (event) => {
        getJSON(`${url}/modes/set?mode=bpm`)
    })

    

}bpm()