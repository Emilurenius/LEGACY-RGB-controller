function adminLogin() {
    const passInput = document.getElementById("passInput")
    const loginButton = document.getElementById("login")

    loginButton.addEventListener("click", (event) => {
        const pass = passInput.value

        if (pass) {
            console.log("pass")
            setCookie("adminPass", pass, 1)
            window.location.reload()
        }
    })
}adminLogin()