const { Worker } = require('worker_threads')
const { exec } = require('node:child_process')
const sleep = require('system-sleep')
const WORKING_FOLDER = process.argv[1].split('/').slice(0, -1).join('/')

let THREAD_COUNT = 4

exec('nproc', (err, output) => {
    if (err) {
        console.log('Could not execute command: ', err)
        console.log(`Could not fetch amount of logical cores. Assuming available core count = ${THREAD_COUNT}`)
        return
    }
    console.log(`Core count confirmed to be ${output}`)
    THREAD_COUNT = parseInt(output)
})



const localPath = (path) => {
    return `${WORKING_FOLDER}/${path}`
}

const animations = {
    colorBubbles: require(localPath('/animations/colorBubbles.js'))
}

animations.colorBubbles.setPixelNum(40)
let animationSpeed = 20
while (true) {
    animations.colorBubbles.changeSettings({speed: animationSpeed})
    console.log(animations.colorBubbles.animationTick())
    sleep(10)
}