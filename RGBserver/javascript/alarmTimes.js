function alarmTimes() {
    const alarmTimeDay = document.getElementById("alarmTimeDay")
    const alarmTimeHour = document.getElementById("alarmTimeHour")
    const alarmTimeMinute = document.getElementById("alarmTimeMinute")

    document.createElement("option")
    let i = 0
    while (i < 24) {
        let option = document.createElement("option")
        option.value = `${i}`
        option.innerHTML = `${i}`
        alarmTimeHour.appendChild(option)
        i++
    }

    i = 0
    while (i < 61) {
        let option = document.createElement("option")
        option.value = `${i}`
        option.innerHTML = `${i}`
        alarmTimeMinute.appendChild(option)
        i++
    }
}

alarmTimes()