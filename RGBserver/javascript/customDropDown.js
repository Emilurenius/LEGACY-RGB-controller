function customDropDown () {
    const expandButtons = document.querySelectorAll("#cddExpandCollapse")

    for(let i=0; i<=expandButtons.length - 1; i++) {
        let dropDownFound = false
        const parent = expandButtons[i].parentElement
        const parentChildren = parent.childNodes

        for(let i=0; i<=parentChildren.length - 1; i++) {
            if (parentChildren[i].classList == undefined) {
                continue
            }

            if (parentChildren[i].classList.contains("customDropDown")) {
                dropDownFound = true
            }
        }

        if (dropDownFound) {
            expandButtons[i].onclick = (event) => {
                console.log(event.target.parentElement)

                for(let i=0; i<=parentChildren.length - 1; i++) {
                    if (parentChildren[i].classList == undefined) {
                        continue
                    }
        
                    if (parentChildren[i].classList.contains("customDropDown") && parentChildren[i].style.display == "none") {
                        parentChildren[i].style.display = "block"
                        event.target.value = "Collapse"
                    }else if (parentChildren[i].classList.contains("customDropDown")) {
                        parentChildren[i].style.display = "none"
                        event.target.value = "Expand"
                    }
                }
            }
        }
    }
}
customDropDown()