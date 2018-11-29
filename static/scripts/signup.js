function populatePrograms(db) {
    var select = document.getElementById("select-program")
    db.ref('catalog').once('value').then(function(snapshot) {
        var keys = Object.keys(snapshot.val())
        window.data = snapshot.val()
        for (var i = 0; i < keys.length; i++) {
            var opt = keys[i]
            var elem = document.createElement("option")
            elem.textContent = opt
            elem.value = opt
            select.appendChild(elem)
        }
    });
}

function populateThreads() {
    var selection = document.getElementById("select-program").value
    var degree = document.querySelector('input[name = "degree"]:checked').value
    var threadsSelector = document.getElementById("select-thread")
    threadsSelector.innerHTML = '<option id="default-thread" value="N/A" disabled selected>N/A</option>'
    
    if (degree === "BS" || degree === "MS") {
        var breakdown = window.data[selection][degree]
        if (breakdown.hasOwnProperty("concentrations")) {
            var concs = Object.keys(breakdown["concentrations"])
            for (var i = 0; i < concs.length; i++) {
                var opt = concs[i]
                var elem = document.createElement("option")
                elem.textContent = opt
                elem.value = opt
                threadsSelector.appendChild(elem)
            }
        } else if (breakdown.hasOwnProperty("threads")) {
            var threads = Object.keys(breakdown["threads"])
            for (var i = 0; i < threads.length; i++) {
                var opt = threads[i]
                var elem = document.createElement("option")
                elem.textContent = opt
                elem.value = opt
                threadsSelector.appendChild(elem)
            }
        }
    }
}

window.onload = function() {
    window.db = initDB()
    populatePrograms(db)
};