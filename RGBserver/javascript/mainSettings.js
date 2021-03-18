const colorChangeMode = document.getElementById("colorChangeModeSelect")

colorChangeMode.addEventListener("change", (event) => {
    console.log(`Current value: ${this.value}`)
    console.log(event)
})