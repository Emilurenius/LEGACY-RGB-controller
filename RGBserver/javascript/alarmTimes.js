function alarmTimes() {
    const alarmTimeDay = document.getElementById("alarmTimeDay")
    const alarmTimeHour = document.getElementById("alarmTimeHour")
    const alarmTimeMinute = document.getElementById("alarmTimeMinute")
    const saveButton = document.getElementById("saveAlarmTimeButton")
    const activeAlarmsContainer = document.getElementById("activeAlarmsContainer")
    let alarms = getJSON(`${url}/json/alarmTimes.json`).times

    function populateAlarmsContainer() {
        activeAlarmsContainer.innerHTML = ""
        alarms = getJSON(`${url}/json/alarmTimes.json`).times
        for (let i = 0; i < alarms.length; i++) {
            const alarmDiv = document.createElement("div")
            alarmDiv.classList.add("Content-subBox")

            const alarmText = document.createElement("p")
            alarmText.classList.add("Body-Text")
            alarmText.innerHTML = alarms[i]

            const deleteButton = document.createElement("button")
            deleteButton.classList.add("button")
            deleteButton.id = alarms[i]

            deleteButton.onclick = (event) => {
                console.log(event.target.id)
            }

            const deleteIcon = document.createElement("i")
            deleteIcon.classList.add("fa")
            deleteIcon.classList.add("fa-trash")
            deleteButton.id = alarms[i]

            deleteButton.appendChild(deleteIcon)
            alarmText.appendChild(deleteButton)

            alarmDiv.appendChild(alarmText)
            activeAlarmsContainer.appendChild(alarmDiv)
        }
        activeAlarmsContainer.appendChild(document.createElement("br"))
    }
    populateAlarmsContainer()

    let i = 0
    while (i < 24) {
        let option = document.createElement("option")
        if (i < 10) {
            option.value = `0${i}`
            option.innerHTML = `0${i}`
        }else {
            option.value = `${i}`
            option.innerHTML = `${i}`
        }
        alarmTimeHour.appendChild(option)
        i++
    }

    i = 0
    while (i < 60) {
        let option = document.createElement("option")
        if (i < 10) {
            option.value = `0${i}`
            option.innerHTML = `0${i}`
        }else {
            option.value = `${i}`
            option.innerHTML = `${i}`
        }
        alarmTimeMinute.appendChild(option)
        i++
    }

    saveButton.addEventListener("click", (event) => {
        const alarmTime = `${alarmTimeDay.value}-${alarmTimeHour.value}-${alarmTimeMinute.value}`
        alarms = getJSON(`${url}/json/alarmTimes.json`).times

        if (alarms.includes(alarmTime)) {
            alert("Alarm time already exists")
        }
        else {
            getJSON(`${url}/alarmTimes/edit?mode=new&alarmTime=${alarmTime}`)
        }
        populateAlarmsContainer()
    })
}

alarmTimes()