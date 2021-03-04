this.onmessage = (e) => {
    let previousCheck = Date.now()
    while (Date.now() > e.data.nextSongAt + 5000) {
        if (previousCheck < Date.now() + 5000) {
            previousCheck = Date.now()
            this.postMessage({response: "checkSong"})
        }
    }

    this.postMessage({response: "song done"})
}