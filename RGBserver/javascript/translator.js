import {translate} from "/javascript/codeify.js"

let translation = getJSON("/json/langs/norwegian.json")

// console.log(translation)
// translate(translation)

for (const key of Object.keys(translation)) {
    if (key.id == false) {
        console.log(`Translating to: ${key.language}`)
    }
    else {
        console.log(key)
        document.getElementById(key.id).innerHTML = key.translation
    }
}