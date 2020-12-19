export function textFormat(rawText, textClass) {
    const textBox = document.createElement("div")
    const bodyTextList = rawText.split("\n")
    let body = document.createElement("p")
    body.classList.add(textClass)
    for (let val of Object.entries(bodyTextList)) {
        const textList = val[1].split(" ")

        for (let command of Object.entries(textList)) {
            command = command[1]
            if (command.startsWith("<")) {
                command = command.replace("<", "")
                command = command.replace(">", "")
                command = command.split(",")

                if (command[0] == "link") {
                    let link = document.createElement("a")
                    link.classList.add("linkStyle")
                    link.href = command[1]
                    const linkText = document.createTextNode(`${command[2]} `)
                    link.appendChild(linkText)
                    body.appendChild(link)
                } 
                else {
                    const text = document.createTextNode(`<${command}> `)
                    body.appendChild(text)
                }
            } 
            else {
                const text = document.createTextNode(`${command} `)
                body.appendChild(text)
            }
        }
        body.appendChild(document.createElement("br"))
    }
    textBox.appendChild(body)
    return textBox
}
