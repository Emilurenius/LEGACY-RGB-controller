function getQueries() {
    const queryString = window.location.search.replace("?", "")
    const queriesList = queryString.split("&")

    let queriesDict = new Object()

    for (let i=0; i<=queriesList.length - 1; i++) {
        const keyValue = queriesList[i].split("=")
        if (keyValue[1]) {
            keyValue[1] = keyValue[1].replace("%20", " ")
        }
        queriesDict[keyValue[0]] = keyValue[1]
    }

    return queriesDict
}

const queries = getQueries()