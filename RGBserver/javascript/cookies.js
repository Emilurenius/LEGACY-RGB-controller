function setCookie(cname, cvalue, exdays) { // Set cookie with set values cname, cvalue and exdays
    const d = new Date()
    d.setTime(d.getTime() + (exdays*24*60*60*1000))
    const expires = `expires=${d.toUTCString()}`
    document.cookie = `${cname}=${cvalue};${expires}:path=/`
}

function getCookie(cname) { // Search for cookie with name of variable cname. If found: return cookie, else: return empty string.
    const name = `${cname}=`
    const decodedCookie = decodeURIComponent(document.cookie)
    const ca = decodedCookie.split(";")
    for (let i = 0; i < ca.length; i ++) {
        let c = ca[i]
        while (c.charAt(0) == " ") {
            c = c.substring(1)
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length)
        }
    }
    return ""
}

if (getCookie("scrollPos") != "") {
    console.log(getCookie("scrollPos"))
    window.pageYOffset = parseInt(getCookie("scrollPos"))
    document.documentElement.scrollTop = parseInt(getCookie("scrollPos"))
}

let previousScrollVal = undefined
function scroll() {
    let top = document.documentElement.scrollTop || window.pageYOffset
    console.log(top)
    if (previousScrollVal == undefined) {
        previousScrollVal = top
    }
    else if (previousScrollVal < 10 && top == 100) {
        top = 0
    }
    setCookie("scrollPos", top, 1)
}

var bodySelector = $("body").first()
console.log(bodySelector.scrollTop())
