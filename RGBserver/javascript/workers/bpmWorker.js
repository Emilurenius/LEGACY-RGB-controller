this.onmessage = (e) => {
    while (Date.now() < e.data.nextSongAt + 5000) {
        continue
    }

    this.postMessage({response: e.data.nextSongAt})
}