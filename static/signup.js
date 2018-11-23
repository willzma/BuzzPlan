function initDB(){
	var config = {
        apiKey: "AIzaSyA3i7m9Y2GDih3V4HS4vywuE94kRj6rhE0",
        authDomain: "buzzplan-d333f.firebaseapp.com",
        databaseURL: "https://buzzplan-d333f.firebaseio.com",
        projectId: "buzzplan-d333f",
        storageBucket: "buzzplan-d333f.appspot.com",
        messagingSenderId: "572769101291"
    };
    var app = firebase.initializeApp(config)
    return app.database()
}

function populate_programs(db) {
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

function populate_threads() {
    var selection = document.getElementById("select-program").value
    var degree = document.querySelector('input[name = "degree"]:checked').value
    var threads_selector = document.getElementById("select-thread")
    if (degree === "BS" || degree === "MS") {
        var breakdown = window.data[selection][degree]
        if (breakdown.hasOwnProperty("concentrations")) {
            var concs = Object.keys(breakdown["concentrations"])
            for (var i = 0; i < concs.length; i++) {
                var opt = concs[i]
                var elem = document.createElement("option")
                elem.textContent = opt
                elem.value = opt
                threads_selector.appendChild(elem)
            }
        } else if (breakdown.hasOwnProperty("threads")) {
            var threads = Object.keys(breakdown["threads"])
            for (var i = 0; i < threads.length; i++) {
                var opt = threads[i]
                var elem = document.createElement("option")
                elem.textContent = opt
                elem.value = opt
                threads_selector.appendChild(elem)
            }
        }
    }
}

window.onload = function() {
    window.db = initDB()
    populate_programs(db)
};