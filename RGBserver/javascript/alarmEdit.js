function alarmEdit() {
    function doubleDigit(val) {
        val = parseInt(val)
        if (val < 10) {
            val = `0${val}`
        }
        return val
    }

    function updateDaysSelect() {
        for (let i = 0; i < daysLookup.length; i++) {
            if (daysSelected[daysLookup[i]] == "true") { // Reformat the true/false strings into booleans
                daysSelected[daysLookup[i]] = true
            }else {
                daysSelected[daysLookup[i]] = false
            }

            if (daysSelected[daysLookup[i]]) {
                document.getElementById(`${daysLookup[i]}Select`).style = "background: black; color: white;"
            }else {
                document.getElementById(`${daysLookup[i]}Select`).style = "background: white; color: black;"
            }
        }
    }

    const daysLookup = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    const alarmName = document.getElementById("alarmName")
    const alarmTimeHour = document.getElementById("alarmTimeHour")
    const alarmTimeMinute = document.getElementById("alarmTimeMinute")
    const daysSelect = document.getElementById("daysSelect")
    const saveButton = document.getElementById("saveAlarmTimeButton")
    const alarmTime = queries.alarmTime

    let daysSelected = {} // Create a dictionary to save what days are selected
    for (let i = 0; i < daysLookup.length; i++) {
        daysSelected[daysLookup[i]] = false
    }

    let i = 0
    while (i < 24) { // Populate dropdown with all 24 hours of the day
        let option = document.createElement("option")
        option.value = doubleDigit(i)
        option.innerHTML = doubleDigit(i)
        alarmTimeHour.appendChild(option)
        i++
    }

    i = 0
    while (i < 60) { // Populate dropdown with all 60 minutes in an hour
        let option = document.createElement("option")
        option.value = doubleDigit(i)
        option.innerHTML = doubleDigit(i)
        alarmTimeMinute.appendChild(option)
        i++
    }

    for (let i = 0; i < daysLookup.length; i++) { // Populate all buttons for selecting days
        const dayButton = document.createElement("button")
        dayButton.innerHTML = daysLookup[i]
        dayButton.classList.add("squareButton")
        dayButton.id = `${daysLookup[i]}Select`
        dayButton.style = "background: white; color: black;"

        dayButton.onclick = (event) => {
            console.log(event.target.innerHTML)
            if (daysSelected[event.target.innerHTML]) {
                event.target.style = "background: white; color: black;"
                daysSelected[event.target.innerHTML] = false
            }
            else {
                event.target.style = "background: black; color: white;"
                daysSelected[event.target.innerHTML] = true
            }
        }
        daysSelect.appendChild(dayButton)
    }

    if (alarmTime) {
        let alarms = getJSON(`${url}/json/alarmTimes.json`)

        console.log(alarms[alarmTime])
        const hourMins = alarms[alarmTime].time.split(":")
        alarmName.value = alarmTime
        alarmTimeHour.value = hourMins[0]
        alarmTimeMinute.value = hourMins[1]
        daysSelected = alarms[alarmTime].days
        updateDaysSelect()
    }else {
        const now = new Date()
        const currentMin = doubleDigit(now.getMinutes())
        const currentHour = doubleDigit(now.getHours())
        const currentDay = now.getDay()
        console.log(`${daysLookup[currentDay]} - ${currentHour}:${currentMin}`)

        alarmTimeHour.value = doubleDigit(currentHour)
        alarmTimeMinute.value = doubleDigit(currentMin)
    }

    saveButton.addEventListener("click", (event) => {
        alarmData = {
            "name": alarmName.value,
            "time": `${alarmTimeHour.value}:${alarmTimeMinute.value}`,
            "days": daysSelected
        }
        console.log(alarmData)
        console.log(postJSON(`${url}/alarm/edit`, alarmData))
    })
}alarmEdit()