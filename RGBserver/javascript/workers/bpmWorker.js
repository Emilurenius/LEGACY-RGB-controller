this.onmessage = (e) => {
    while (Date.now() < e.data.nextSongAt) {
        continue
    }

    this.postMessage({response: e.data.nextSongAt})
}