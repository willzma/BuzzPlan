function initDB(){
	var config = {
        apiKey: "AIzaSyA3i7m9Y2GDih3V4HS4vywuE94kRj6rhE0",
        authDomain: "buzzplan-d333f.firebaseapp.com",
        databaseURL: "https://buzzplan-d333f.firebaseio.com",
        projectId: "buzzplan-d333f",
        storageBucket: "buzzplan-d333f.appspot.com",
        messagingSenderId: "572769101291"
    };
    var app = firebase.initializeApp(config);

    return app.database()
}

function preparePrerequisiteData(db, course_name){
	var data_promise = db.ref('/prerequisite_map').child(course_name).once('value')
	.then( function(value) {
		var all_promise = []
		var cls_list = value.val()
		var prerequiiste_ref = db.ref('/Prerequisites')
		for (var i = 0; i < cls_list.length; i++){
			all_promise.push(prerequiiste_ref.child(cls_list[i]).once('value')
			.then( function (value){
				return value.val()
			}))
		}

		return Promise.all(all_promise)
		.then(function (values){
			data = {}
			for (var i = 0; i < cls_list.length; i++){
				data[cls_list[i]] = values[i]
			}
			return data
		})
	})


	return data_promise
}

//function 