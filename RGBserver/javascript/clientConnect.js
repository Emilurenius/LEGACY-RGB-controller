function clientConnect() {
    codeInput = document.getElementById("codeInput")
    codeSubmit = document.getElementById("codeSubmit")

    codeSubmit.addEventListener("click", (event) => {
        const connectCode = codeInput.value
        console.log(connectCode)
        setCookie("connectCode", connectCode, 1)
        window.location.reload()
    })
}
clientConnect()