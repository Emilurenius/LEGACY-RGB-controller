import {translate} from "/javascript/codeify.js"
const langSelector = document.getElementById("lang-select")

let norwegian = getJSON("/json/langs/norwegian.json")

langSelector.addEventListener("change", () => {
    console.log(`Translating to: ${langSelector.value}`)

    if (this.value == "NOB") {
        console.log(norwegian)
        translate(norwegian)
    }
})