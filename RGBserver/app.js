// All external modules are loaded in:
const express = require("express")
const app = express()
const path = require("path")
const fs = require("fs")
const cors = require("cors")
const port = 3000
var counter = 0

app.use(cors()) // Making sure the browser can request more data after it is loaded on the client computer.

// JSON file loaded in before the server is started:
let rawdata = fs.readFileSync("./json/data.json")
let data = JSON.parse(rawdata)
console.log(`Data loaded: ${data}`)

// All server folders are set up:
app.use("/css", express.static("css"))
app.use("/javascript", express.static("javascript"))
app.use("/json", express.static("json"))

// All adresses are defined:
app.get("/", (req, res) => {
    console.log("\nControl panel loaded")
    let save = false
    res.sendFile(path.join(__dirname, "/html/index.html"))
    
    if (req.query.toggle == "change") {
        if (data.onoff == true) {
            data.onoff = false
            save = true
        }else {
            data.onoff = true
            save = true
        }
        console.log(`Light state changed to: ${data.onoff}`)
    }
    
    if (req.query.br) {
        data.brightness = parseInt(req.query.br)
        console.log(`BR changed to: ${data.brightness}`)
        save = true
    }
    if (req.query.r) {
        data.R = parseInt(req.query.r)
        console.log(`R changed to: ${data.R}`)
        save = true
    }
    if (req.query.g) {
        data.G = parseInt(req.query.g)
        console.log(`G changed to: ${data.G}`)
        save = true
    }
    if (req.query.b) {
        data.B = parseInt(req.query.b)
        console.log(`B changed to: ${data.B}`)
        save = true
    }
    
    if (save) {
        let stringified = JSON.stringify(data, null, 2)
    
        fs.writeFile("./json/data.json", stringified, (err) => {
            if (err) throw err
            console.log("Data written to file")
        })
    }
    
})

app.get("/lightstate", (req, res) => {
    if (data.onoff) {
        res.send("true")
    }else {
        res.send("false")
    }
})

app.get("/br", (req, res) => {
    res.send(data.brightness.toString())
})

app.get("/r", (req, res) => {
    res.send(data.R.toString())
})

app.get("/g", (req, res) => {
    res.send(data.G.toString())
})

app.get("/b", (req, res) => {
    res.send(data.B.toString())
})

app.get("/rgb", (req, res) => { // This is for API control of the lights without the server sending a webpage as a response.
    console.log("API loaded: RGB")

    let save = false
    if (req.query.br) {
        data.brightness = parseInt(req.query.br)
        console.log(`BR changed to: ${data.brightness}`)
        save = true
    }
    if (req.query.r) {
        data.R = parseInt(req.query.r)
        console.log(`R changed to: ${data.R}`)
        save = true
    }
    if (req.query.g) {
        data.G = parseInt(req.query.g)
        console.log(`G changed to: ${data.G}`)
        save = true
    }
    if (req.query.b) {
        data.B = parseInt(req.query.b)
        console.log(`B changed to: ${data.B}`)
        save = true
    }
    
    if (save) {
        let stringified = JSON.stringify(data, null, 2)
    
        fs.writeFile("./json/data.json", stringified, (err) => {
            if (err) throw err
            console.log("Data written to file")
        })
        res.send("data sent")
    } else {
        res.send("no data recieved")
    }
})

app.get("/modes/set", (req, res) => {
    console.log("API loaded: Mode select")

    let save = false
    if (req.query.mode) {
        save = true
        data.mode = req.query.mode
    }
})

app.get("/modes", (req, res) => {
    console.log("\nMode select loaded")
    let save = false
    res.sendFile(path.join(__dirname, "/html/modes.html"))
    
    if (req.query.mode != undefined) {
        save = true
        data.mode = req.query.mode
        console.log(`Mode changed to: ${data.mode}`)
    }
    
    if (req.query.speed) {
        save = true
        data.breatheSpeed = parseInt(req.query.bSpeed)
        console.log(`Speed channged to: ${data.speed}`)
    }
    
    if (save) {
        let stringified = JSON.stringify(data, null, 2)
    
        fs.writeFile("./json/data.json", stringified, (err) => {
            if (err) throw err
            console.log("Data written to file")
        })
    }
})



app.listen(port, () => console.log(`Listening on ${port}`))
