import {translate} from "/javascript/codeify.js"

let translation = getJSON("/json/langs/norwegian.json")

// console.log(translation)
// translate(translation)

for (let key of Object.keys(translation)) {
    if (key == "header") {
        console.log(`Translating to: ${translation[key].language}`)
    }
    else {
        console.log(key)
        document.getElementById(key).innerHTML = translation[key]
    }
}