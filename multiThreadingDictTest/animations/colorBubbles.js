const { Worker } = require('worker_threads')

const WORKING_FOLDER = process.argv[1].split('/').slice(0, -1).join('/')

function colorBubbles () {
    const name = 'colorBubbles.js'
    let numPixels = 0
    let stripBrightness = {}
    let animationSettings = {
        speed: 10,
        tailLength: 5,
        bubbleDistance: 5
    }

    this.setPixelNum = (pixelNum) => {
        numPixels = pixelNum
        stripBrightness = {}
        for (let i = 0; i < pixelNum; i++) {
            stripBrightness[i] = {
                val: 0,
                up: true,
                active: false
            }
        }
    }

    this.changeSettings = (args) => {
        if ('speed' in args) {
            animationSettings.speed = args.speed
        }
        if ('tailLength' in args) {
            animationSettings.tailLength = args.tailLength
        }
        if ('bubbleDistance' in args) {
            animationSettings.bubbleDistance = args.bubbleDistance
        }

        return animationSettings
    }

    this.animationTick = () => {
        noneActive = true
        for (let i = 0; i < animationSettings.bubbleDistance; i++) {
            if (stripBrightness[i].active == true) {
                noneActive = false
                break
            }
        }
        if (noneActive) {
            stripBrightness[0].active = true
        }

        for (let i = 0; i < numPixels; i++) {

            // Fade pixel up:
            if (stripBrightness[i].up == true && stripBrightness[i].val < 1000 && stripBrightness[i].active) {
                stripBrightness[i].val += animationSettings.speed

                if (stripBrightness[i].val >= 1000) { // Activate next pixel
                    stripBrightness[i].val = 1000
                    if (stripBrightness[i+1] != undefined) { // Make sure next pixel actually exists
                        stripBrightness[i+1].active = true
                    }
                }
            }

            // Fade pixel down
            else if (stripBrightness[i].active && stripBrightness[i].val > 0) {
                stripBrightness[i].up = false
                stripBrightness[i].val -= animationSettings.speed / animationSettings.tailLength

                if (stripBrightness[i].val <= 0) { // Reset pixel
                    stripBrightness[i].val = 0
                    stripBrightness[i].active = false
                    stripBrightness[i].up = true
                }
            }
        }
        return stripBrightness
    }
}

module.exports = new colorBubbles()