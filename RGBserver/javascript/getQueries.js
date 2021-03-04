function getQueries() {
    const queryString = window.location.search.replace("?", "")
    const queriesList = queryString.split("&")

    let queriesDict = new Object()

    for (let i=0; i<=queriesList.length - 1; i++) {
        const keyValue = queriesList[i].split("=")
        console.log(keyValue)
        queriesDict[keyValue[0]] = keyValue[1]
    }

    return queriesDict
}

const queries = getQueries()
console.log(queries)