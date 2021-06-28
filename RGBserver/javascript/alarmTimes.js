function alarmTimes() {

    function dayColorLookup(state) {
        if (state) {
            return "color: white;"
        }else {
            return "color: black;"
        }
    }

    function formatDays(days) {
        for (let i = 0; i < daysLookup.length; i++) {
            if (days[daysLookup[i]] == "true") { // Reformat the true/false strings into booleans
                days[daysLookup[i]] = true
            }else {
                days[daysLookup[i]] = false
            }
        }
        return days
    }

    const createNewAlarm = document.getElementById("createNewAlarm")
    createNewAlarm.href = `${url}/alarm/edit`

    const daysLookup = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    const alarmContainer = document.getElementById("alarmContainer")
    console.log(alarmContainer)
    let alarms = getJSON(`${url}/json/alarmTimes.json`)

    for ([key, val] of Object.entries(alarms)) {
        const container = document.createElement("div")
        container.classList.add("Content-box")

        const editButton = document.createElement("a")
        editButton.classList.add("button")
        editButton.style = "float: right;"
        editButton.innerHTML = "Edit"
        editButton.href = `${url}/alarm/edit?alarmTime=${key}`
        container.appendChild(editButton)

        alarms[key].days = formatDays(alarms[key].days)
        console.log(key, val)

        const alarmName = document.createElement("p")
        alarmName.classList.add("Body-Text")
        alarmName.innerHTML = key
        container.appendChild(alarmName)

        const dayshours = document.createElement("p")
        dayshours.classList.add("Body-Text-alignLeft")
        for (let i = 0; i < daysLookup.length; i++) {
            const daySpan = document.createElement("span")
            daySpan.innerHTML = `${daysLookup[i]} `
            daySpan.style = dayColorLookup(val.days[daysLookup[i]])
            dayshours.appendChild(daySpan)
        }

        const hourmins = document.createElement("span")
        hourmins.innerHTML = `&nbsp; &nbsp;${val.time}`
        dayshours.appendChild(hourmins)
        container.appendChild(dayshours)

        alarmContainer.appendChild(container)
    }
}

alarmTimes()