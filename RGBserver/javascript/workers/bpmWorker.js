this.onmessage = (e) => {
    while (Date.now() < e.data.nextSongAt + 1000) {
        continue
    }

    this.postMessage({response: e.data.nextSongAt})
}