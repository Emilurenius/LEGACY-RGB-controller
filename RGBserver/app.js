// All external modules are loaded in:
const express = require("express")
const app = express()
const bodyParser = require("body-parser")
const path = require("path")
const fs = require("fs")
const cors = require("cors")

function loadJSON(filename) {
    const rawdata = fs.readFileSync(path.join(__dirname, filename))
    const data = JSON.parse(rawdata)
    return data
}

function saveJSON(json, filename) {
    const stringified = JSON.stringify(json, null, 4)
    fs.writeFile(path.join(__dirname, filename), stringified, (err) => {
        if (err) throw err
        console.log("Data written to file")
    })
}

// Reading input from terminal start
const port = parseInt(process.argv[2])
console.log(`${port} registered as server port`)
// Reading input from terminal end

// Variables set up for long polling address:
const LIMIT = 20
const DELAY = 1000
let tick = 0
let connections = [] // Connections through long polling

//Here we are configuring express to use body-parser as middle-ware.
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.use(cors()) // Making sure the browser can request more data after it is loaded on the client computer.

// JSON file loaded in before the server is started:
let data = loadJSON("/json/data.json")
console.log(`Data loaded: ${data}`)

// Initializing directRGB json file
const pixelCount = 149
let pixelData = {}
for (let i = 0; i < pixelCount; i++) {
    pixelData[i] = [0,0,0]
}
saveJSON(pixelData, "/json/directRGB.json")

// All server folders are set up:
app.use("/css", express.static("css"))
app.use("/javascript", express.static("javascript"))
app.use("/json", express.static("json"))

// Graphical control interface:
app.get("/", (req, res) => {
    
    res.sendFile(path.join(__dirname, "/html/index.html"))
    console.log("\nWebsite loaded")
    
    if (req.query.panel == "main") {
        console.log("\nControl panel loaded")
        let save = false

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
            saveJSON(data, "/json/data.json")
        }
    }
    else if (req.query.panel == "modes") {
        console.log("\nMode select loaded")
        let save = false

        if (req.query.mode != undefined) {
            save = true
            data.mode = req.query.mode
            console.log(`Mode changed to: ${data.mode}`)
        }
        
        if (req.query.speed) {
            save = true
            data.speed = parseInt(req.query.speed)
            console.log(`Speed channged to: ${data.speed}`)
        }
    
        if (req.query.alarmTime) {
            save = true
            data.alarmClockData.alarmTime = req.query.alarmTime
            console.log(`Alarm set to activate at: ${data.alarmClockData.alarmTime}`)
        }
        
        if (save) {
            saveJSON(data, "/json/data.json")
        }
    }
    
})

app.get("/settings", (req, res) => {
    res.sendFile(path.join(__dirname, "/html/settings.html"))
})

app.get("/alarm", (req, res) => {
    res.sendFile(path.join(__dirname, "/html/alarm.html"))
})

app.get("/alarm/edit", (req, res) => {
    res.sendFile(path.join(__dirname, "/html/alarmEdit.html"))
})

// API GET:
app.get("/lightstate", (req, res) => {
    console.log("\nAPI loaded: Lightstate")
    save = false

    if (req.query.toggle == "change") {
        if (data.onoff == true) {
            data.onoff = false
            save = true
        }
        else {
            data.onoff = true
            save = true
        }
        console.log(`Light state changed to: ${data.onoff}`)
    }

    if (save) {
        saveJSON(data, "/json/data.json")
    }

    if (data.onoff) {
        res.send(true)
    }else {
        res.send(false)
    }
})

app.get("/checklightstate", (req, res) => {
    if (data.onoff) {
        res.send(true)
    }else {
        res.send(false)
    }
})

app.get("/br", (req, res) => {
    console.log("\nAPI loaded: Send brightness")
    res.send(data.brightness.toString())
})

app.get("/r", (req, res) => {
    console.log("\nAPI loaded: Send red")
    res.send(data.R.toString())
})

app.get("/g", (req, res) => {
    console.log("\nAPI loaded: Send green")
    res.send(data.G.toString())
})

app.get("/b", (req, res) => {
    console.log("\nAPI loaded: Send blue")
    res.send(data.B.toString())
})

app.get("/rgb", (req, res) => {
    console.log("\nAPI loaded: RGB")

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
        saveJSON(data, "/json/data.json")
        res.send("data recieved")
    } else {
        res.send("no data recieved")
    }
})

app.get("/modes/set", (req, res) => {
    console.log("\nAPI loaded: Mode select")

    let save = false
    if (req.query.mode) {
        save = true
        data.mode = req.query.mode
    }

    if (req.query.elitusMode) {
        save = true
        data.eliteData.mode = req.query.elitusMode
    }

    if (save) {
        saveJSON(data, "/json/data.json")
        res.send(`Data recieved: mode changed to ${data.mode}`)
    } else {
        res.send("no data recieved")
    }
})

app.get("/modes/current", (req, res) => {
    res.send(`${data.mode}`)
})

app.get("/colorpresets", (req, res) => {
    console.log(`\nPreset API loaded:`)

    if (req.query.mode == "new") {
        console.log("New preset being generated")
        let presetRawData = fs.readFileSync(path.join(__dirname, "/json/presets.json"))
        let presetData = JSON.parse(presetRawData)

        presetData[req.query.presetName] =  {
            "R": req.query.R,
            "G": req.query.G,
            "B": req.query.B
        }

        saveJSON(presetData, "/json/presets.json")
        res.send("Success")
    }
    else if (req.query.mode == "load") {
        res.sendFile(path.join(__dirname, "/json/presets.json"))
    }
})

app.get("/bpm", (req, res) => {
    console.log("\nBPM API loaded:")
    if (req.query.mode == "getBPM") {
        res.sendFile(path.join(__dirname, "/json/bpm.json"))
    }
    else if (req.query.mode == "updateBPM") {
        const rawData = fs.readFileSync(path.join(__dirname, "/json/bpm.json"))
        const bpmData = JSON.parse(rawData)

        bpmData.value = req.query.bpm
        bpmData.syncDelay = 0
        console.log(`Current BPM: ${bpmData.value}`)

        saveJSON(bpmData, "/json/bpm.json")
        res.send("Success")
    }
    else if (req.query.mode  == "resetDelay") {
        const rawData = fs.readFileSync(path.join(__dirname, "/json/bpm.json"))
        const bpmData = JSON.parse(rawData)
        bpmData.syncDelay = 0
        saveJSON(bpmData, "/json/bpm.json")
        res.send("Success")
    }
    else if (req.query.mode == "spotifySync") {
        res.redirect("http://192.168.1.124:8000/getBPM")
    }
    else if (req.query.mode == "spotifyResponse") {
        console.log("\nSpotify sync response recieved:")
        const rawData = fs.readFileSync(path.join(__dirname, "/json/bpm.json"))
        const bpmData = JSON.parse(rawData)
        bpmData.value = parseFloat(req.query.bpm)

        const sinceSent = Date.now() - parseInt(req.query.messageSent)
        const currentSongProgress = parseInt(req.query.songProgress) + sinceSent
        
        const waitTimeMS = (60 / bpmData.value) * 1000
        let activateAt = 0
        do {
            activateAt = activateAt + waitTimeMS
        }while (activateAt < currentSongProgress + 100)
        const activateIn = activateAt - currentSongProgress // In milliseconds
        bpmData.syncDelay = (Date.now() + activateIn) / 1000

        console.log(`Current song progress: ${currentSongProgress}\nActivate in: ${activateIn}`)


        saveJSON(bpmData, "/json/bpm.json")

        res.send(`${bpmData.value}`)
    }
})

app.get("/settings/standard", (req, res) => {
    console.log("\nStandard settigns API loaded")
    let rawdata = fs.readFileSync(path.join(__dirname, "/json/standardSettings.json"))
    let standardSettings = JSON.parse(rawdata)
    let save = false

    if (req.query.colorChange) {
        console.log(`new colorChange value: ${req.query.colorChange}`)
        save = true
        standardSettings.colorChange = req.query.colorChange
    }

    if (save) {
        saveJSON(standardSettings, "/json/standardSettings.json")
    }

    res.sendFile(path.join(__dirname, "/json/standardSettings.json"))
})

// API POST:
app.post("/directRGB", (req, res) => {
    console.log(req.body)
    res.send(req.body)

    for (x in req.body) {
        if (isNaN(x)) {
            console.log(`skipped ${x}: Key is not a number`)
            continue
        }
        else if (parseInt(x) > pixelCount -1 || parseInt(x) < 0) {
            console.log(`skipped ${x}: Index out of range`)
            continue
        }
        else if (typeof req.body[x] != "object") {
            console.log(`skipped ${x}: RGB data not present`)
            continue
        }
        else if (req.body[x].length != 3) {
            console.log(`skipped ${x}: Not all RGB channels are present`)
            continue
        }
        if (isNaN(req.body[x][0]) || isNaN(req.body[x][1]) || isNaN(req.body[x][2])) {
            console.log(`skipped ${x}: RGB values not integers`)
            continue
        }
        else if (req.body[x][0] < 0 || req.body[x][0] > 255 || req.body[x][1] < 0 || req.body[x][1] > 255 || req.body[x][2] < 0 || req.body[x][2] > 255) {
            console.log(`skipped ${x}: RGB values out of range`)
            continue
        }
        pixelData[x] = req.body[x]
    }

    saveJSON(pixelData, "/json/directRGB.json")
})

app.post("/alarm/edit", (req, res) => {
    let alarmTimes = loadJSON("/json/alarmTimes.json")
    alarmTimes[req.body.name] = {
        "time": req.body.time,
        "days": {
            "SUN": req.body["days[SUN]"],
            "MON": req.body["days[MON]"],
            "TUE": req.body["days[TUE]"],
            "WED": req.body["days[WED]"],
            "THU": req.body["days[THU]"],
            "FRI": req.body["days[FRI]"],
            "SAT": req.body["days[SAT]"]
        }
    }
    saveJSON(alarmTimes, "/json/alarmTimes.json")
    res.send(alarmTimes)
})

app.post("/alarm/delete", (req, res) => {
    let alarmTimes = loadJSON("/json/alarmTimes.json")
    delete alarmTimes[req.body.name]

    saveJSON(alarmTimes, "/json/alarmTimes.json")
    res.send(alarmTimes)
})

// Longpolling:
app.get("/reqdata", (req, res, next) => { // this is a long polling address for sending LED strip data to other devices
    res.setHeader("Content-Type", "text/html; charset=utf-8")
    res.setHeader("Transfer-Encoding", "chunked")

    connections.push(res)
})

setTimeout(function run() { // Timeout function for long polling
    if (++tick > LIMIT) {
        connections.map(res => {
            console.log(res)
            res.write("END\n")
            res.end()
        })
        connections = []
        tick = 0
    }
    connections.map((res, i) => {
        res.write(`Connected ${i}`)
    })
    setTimeout(run, DELAY)
}, DELAY)



app.listen(port, () => console.log(`Listening on ${port}`))