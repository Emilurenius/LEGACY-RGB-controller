import {translate} from "/javascript/codeify.js"

let translation = getJSON("/json/langs/norwegian.json")

console.log(translation)
translate(translation)