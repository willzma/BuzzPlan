function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function testLoad(){
    console.log(window.userData);
}

window.onload = function() {
    window.db = initDB();
    if (username != '#'){
        getDatabyKey(db, 'users', username)
        .then(function (value){
            window.userData = value;
            if (!window.userData.hasOwnProperty('courseHistory')){
                window.userData['courseHistory'] = new Set([]);
            }else{
                window.userData['courseHistory'] = new Set(window.userData['courseHistory']);
            }

            document.getElementById('signupbtn').remove();
            document.getElementById('signinbtn').remove();

            var userElement = document.createElement('div');
            userElement.setAttribute('class' ,'headernode');
            userElement.setAttribute('id', 'usergreeting');

            var span = document.createElement('span');
            span.setAttribute('class', 'headercontent');
            span.appendChild(document.createTextNode('Hello! ' + window.userData['username']));
            userElement.appendChild(span);

            document.getElementById('headerdiv').appendChild(userElement);

            // TODO:
            // 1. Show the previous schedule
            // 2. init graph

            var course_name = 'CS 7641';
            var container_id = 'graph-content'

            show_prerequisites(container_id, course_name, window.userData['courseHistory'], db)
        });
    }
};

