const serverValueReset = document.getElementById("serverValueReset")

serverValueReset.addEventListener("click", (evt) => {
    const serverState = getJSON(`${url}/json/data.json`)
    console.log(serverState)
})