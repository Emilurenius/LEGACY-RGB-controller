function alarmTimes() {
    const alarmTimeDay = document.getElementById("alarmTimeDay")
    const alarmTimeHour = document.getElementById("alarmTimeHour")
    const alarmTimeMinute = document.getElementById("alarmTimeMinute")
    const saveButton = document.getElementById("saveAlarmTimeButton")

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
        const alarms = getJSON(`${url}/json/alarmTimes.json`).times

        if (alarms.includes(alarmTime)) {
            alert("Alarm time already exists")
        }
        else {
            getJSON(`${url}/alarmTimes?mode=new&alarmTime=${alarmTime}`)
        }
    })
}

alarmTimes()