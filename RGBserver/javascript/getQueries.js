function getQueries() {
    const queryString = window.location.search
    const queriesList = queryString.split("&")
    return queriesList
}

const queries = getQueries()
console.log(queries)