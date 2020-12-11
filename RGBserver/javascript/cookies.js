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

let scrollPos = getCookie("scrollPos")

if (scrollPos != "") {
    window.pageYOffset = parseInt(scrollPos)
    document.documentElement.scrollTop = parseInt(scrollPos)
} else {
    window.pageYOffset = 0
    document.documentElement.scrollTop = 0
}

var runOnScroll = (evt) => {
    setCookie("scrollPos", window.pageYOffset, 1)
    scrollPos = window.pageYOffset
}

var elements = document.querySelectorAll("...")
elements = Array.prototype.slice.call(elements)

elements.forEach( (element) => {
    window.addEventListener("scroll", runOnScroll, {passive: true})
})