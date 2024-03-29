// All external modules are loaded in:
const express = require("express")
const app = express()
const bodyParser = require("body-parser")
const path = require("path")
const fs = require("fs")
const cors = require("cors")
const cookieParser = require("cookie-parser")
const bcrypt = require("bcrypt")

const SpotifyWebAPI = require('spotify-web-api-node');
scopes = ["user-read-playback-state"]

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

function refreshAccessToken() {
    spotifyAPI.refreshAccessToken().then(
        (data) => { 
            console.log("Access token refreshed")

            spotifyAPI.setAccessToken(data.body["access_token"])
        },
        (err) => {
            console.log("Could not refresh access token", err)
        }
    )
}

const clientData = loadJSON("/spotifyClientData.json")
const spotifyAPI = new SpotifyWebAPI({
    clientId: clientData.clientID,
    clientSecret: clientData.clientSecret,
    redirectUri: clientData.loginRedirect
})
console.log(clientData)

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
app.use(cookieParser()) // Middleware for handling cookies

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
    
    const pass = req.cookies.adminPass
    let passCorrect = false
    console.log(pass)
    const hashedPass = loadJSON("/adminPass/pass.json").pass

    try{
        if (pass) {
            bcrypt.compare(pass, hashedPass, (err, result) => {
                if (err) {
                    res.send("Oops! Something went wrong!<br>Please contact system administrator!")
                    throw new Error(err)
                }else {
                    passCorrect = result
                }
                if (passCorrect) {
                    res.sendFile(path.join(__dirname, "/html/index.html"))
                    console.log("admin logged in successfully")
                } else {
                    res.sendFile(path.join(__dirname, "/html/loginPage.html"))
                    console.log("Login initiated")
                }
            })
        }
        else {
            res.sendFile(path.join(__dirname, "/html/loginPage.html"))
            console.log("Login initiated")
        }
    } catch (err) {
        console.log(`An error has occured: ${err.message}\nAttempting login`)

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

app.get("/speed", (req, res) => {
    console.log("\nAPI loaded: animation speed")

    let save = false
    if (req.query.speed) {
        save = true
        data.speed = parseInt(req.query.speed)
    }
    console.log(data.speed)
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
    else if (req.query.mode == "delete") {
        presetData = loadJSON("/json/presets.json")

        if (presetData[req.query.preset]) {
            delete presetData[req.query.preset]
            saveJSON(presetData, "/json/presets.json")
            res.sendFile(path.join(__dirname, "/json/presets.json"))
        }else {
            res.status(400).send("Error: no preset provided")
        }
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
        bpmData.doneAt = 0
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
})

app.get('/spotify/login', (req, res) => {
    const loginPage = spotifyAPI.createAuthorizeURL(scopes)
    res.redirect(`${loginPage}`)
    console.log("Login initiated")
})

app.get("/spotify/login/success", async (req, res) => {
    const { code } = req.query

    try {
        const data = await spotifyAPI.authorizationCodeGrant(code)
        const { access_token, refresh_token } = data.body
        spotifyAPI.setAccessToken(access_token)
        spotifyAPI.setRefreshToken(refresh_token)

        // res.send(`Logged in! ${access_token} ${refresh_token}`)
        res.redirect("/settings")
        console.log("Logged in")
    } catch (err) {
        res.send("Oops, something went wrong")
        console.log("Login failed")
    }
})

app.get("/spotify/songProgress", async (req, res) => {
    try {
        const result = await spotifyAPI.getMyCurrentPlayingTrack()
        const trackID = result.body.item.id

        const features = await spotifyAPI.getAudioFeaturesForTrack(trackID)
        const tempo = features.body.tempo
        const songProgress = parseInt(result.body.progress_ms)
        const messageSent = parseInt(result.body.timestamp) + songProgress
        const sinceSent = Date.now() - messageSent
    } catch (err) {
        refreshAccessToken()
        res.redirect(`/spotify/songProgress`)
    }
})

app.get("/spotify/getBPM", async (req, res) => {
    try {
        const result = await spotifyAPI.getMyCurrentPlayingTrack()
        const trackID = result.body.item.id

        const features = await spotifyAPI.getAudioFeaturesForTrack(trackID)
        const tempo = features.body.tempo
        const songProgress = parseInt(result.body.progress_ms)
        const messageSent = parseInt(result.body.timestamp) + songProgress
        const sinceSent = Date.now() - messageSent
        console.log(messageSent, Date.now())
        console.log("Since sent:", sinceSent)
        const currentSongProgress = songProgress + sinceSent
        console.log("Current song progress:", currentSongProgress)

        res.status(200).send({
            "tempo": tempo,
            "songProgress": songProgress,
            "messageSent": messageSent
        })

        bpmData = loadJSON("/json/bpm.json")
        bpmData.value = parseFloat(tempo)
        const waitTimeMS = (60 / parseFloat(tempo)) * 1000
        let activateAt = 0

        do {
            activateAt = activateAt + waitTimeMS
        }while (activateAt < currentSongProgress + 100)
        const activateIn = activateAt - currentSongProgress // In milliseconds
        bpmData.syncDelay = parseFloat((Date.now() + activateIn) / 1000)

        console.log(`Current song progress: ${currentSongProgress} ms\nActivate in: ${activateIn} ms`)

        const songDoneAt = Date.now() + features.body.duration_ms - currentSongProgress
        console.log("Song done at:", songDoneAt)
        bpmData.doneAt = songDoneAt

        console.log(bpmData)
        saveJSON(bpmData, "/json/bpm.json")

    } catch (err) {
        refreshAccessToken()
        res.redirect(`/spotify/getBPM`)
    }
})

app.get("/spotify/getAnalysis", async (req, res) => {
    try {
        const result = await spotifyAPI.getMyCurrentPlayingTrack()
        const trackID = result.body.item.id

        const analysis = await spotifyAPI.getAudioAnalysisForTrack(trackID)
        res.send(analysis)

    } catch (err) {
        refreshAccessToken()
        res.redirect(`/spotify/getAnalysis`)
    }
})

app.get("/settings/standard", (req, res) => {
    console.log("\nStandard settigns API loaded")
    let standardSettings = loadJSON("/json/standardSettings.json")
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

app.get("/settings/bpm", (req, res) => {
    console.log("\nBPM settings API loaded:")
    let bpmSettings = loadJSON("/json/bpmSettings.json")
    let save = false

    if (req.query.animationType) {
        bpmSettings.animationType = req.query.animationType
        save = true
    }

    if (save) {
        saveJSON(bpmSettings, "/json/bpmSettings.json")
    }

    res.sendFile(path.join(__dirname, "/json/bpmSettings.json"))
})

app.get("/settings/colorBubbles", (req, res) => {
    console.log("\nColor Bubbles API loaded:")
    let colorBubblesSettings = loadJSON("/json/colorBubblesSettings.json")
    let save = false

    if (req.query.tLength) {
        colorBubblesSettings.tailLength = parseInt(req.query.tLength)
        save = true
    }
    if (req.query.bDist) {
        colorBubblesSettings.bubbleDistance = parseInt(req.query.bDist)
        save = true
    }

    if (save) {
        saveJSON(colorBubblesSettings, "/json/colorBubblesSettings.json")
    }

    res.sendFile(path.join(__dirname, "/json/bpmSettings.json"))
})

app.get("/directRGB", (req, res) => { // A simpler version of the directRGB post address. Should only be used if POST requests are not possible in your usecase
    let pixelData = loadJSON("/json/directRGB.json")
    let save = false
    
    if (req.query.mode == "pixel" && parseInt(req.query.i) < pixelCount - 1) {
        pixelData[req.query.i] = [req.query.r,req.query.g,req.query.b]
        res.send(pixelData[req.query.i])
        save = true
    }
    else {
        console.log(req.query.mode, req.query.i)
        res.send("Invalid data recieved")
    }

    if (save) {
        saveJSON(pixelData, "/json/directRGB.json")
    }
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

// misc:
app.get("/ping", (req, res) => {
    res.send(
        {
            serverName: "lightController"
        }
    )
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