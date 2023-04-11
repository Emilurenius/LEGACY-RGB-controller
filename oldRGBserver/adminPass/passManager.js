const bcrypt = require("bcrypt")
const path = require("path")
const fs = require("fs")

function saveJSON(json, filename) {
    const stringified = JSON.stringify(json, null, 4)
    fs.writeFile(path.join(__dirname, filename), stringified, (err) => {
        if (err) throw err
        console.log("Data written to file")
    })
}

function loadJSON(filename) {
    const rawdata = fs.readFileSync(path.join(__dirname, filename))
    const data = JSON.parse(rawdata)
    return data
}

const mode = process.argv[2]

if (mode == "resetPass") {
    const unHashed = process.argv[3]

    if (unHashed == undefined) {
        console.log("Error: No password provided")
        process.exit(1)
    }

    bcrypt.hash(unHashed, 10).then((hash) => {
        const hashedPass = hash
        console.log(`\nPassword hashed:\n\nOriginal : ${unHashed}\nHashed   : ${hashedPass}`)
        saveJSON({"pass": hashedPass}, "/pass.json")
    })
}
else if (mode == "checkPass") {
    const unHashed = process.argv[3]

    if (unHashed == undefined) {
        console.log("Error: No password provided")
        process.exit(1)
    }

    const hashed = loadJSON("/pass.json").pass
    bcrypt.compare(unHashed, hashed, (err, result) => {
        if (err) {
            console.log(err)
        }else {
            console.log(result)
        }
    })
}