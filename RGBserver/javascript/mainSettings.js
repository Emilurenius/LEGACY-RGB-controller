const colorChangeMode = document.getElementById("colorChangeModeSelect")

colorChangeMode.addEventListener("change", (event) => {
    console.log(`Current value: ${colorChangeMode.options[colorChangeMode.selectedIndex].value}`)
    console.log(event)
    getJSON(`${url}/settings/standard?colorChange=${colorChangeMode.options[colorChangeMode.selectedIndex].value}`)
})

window.onload = () => {
    const settings = getJSON(`${url}/json/standardSettings.json`)

    colorChangeMode.value = settings.colorChange
}