function getQueries() {
    const queryString = window.location.search
    const queriesList = queryString.split("&")
    console.log(queriesList)
}