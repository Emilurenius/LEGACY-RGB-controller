const url = (new URL(document.location)).origin

function getJSON(url) {
    var j = []
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) { j = data },
        async: false
    })
    return j
}

function postJSON(url, JSON) {
    var j = []
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: JSON,
        success: (data) => { j = data },
        async: false
    })
    return j
}