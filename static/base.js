var CALENDAR_START = 480 // 8:00 AM in minutes
var CALENDAR_END = 1320 // 10:00 PM in minutes
var CALENDAR_RANGE = CALENDAR_END - CALENDAR_START

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


// Tue: 9:15 - 11:15   startTime = ((9 * 60) + 15)
// addClass(2, 60, 75, name, location)
/**
 * Adds a course bubble to the calendar (visually).
 * 
 * @param {*} code - abbreviation and course number; e.g. 'CS 6400'
 * @param {*} day - numeric day from Monday - Friday, 0 - 4 respectively
 * @param {*} startTime - the start time of the course in minutes
 * @param {*} duration - duration of the course in minutes
 * @param {*} location - location where the course is being held
 */
function addClass(code, day, startTime, duration, location) {
    var div1 = document.createElement('div');
    var div2 = document.createElement('div');
    var div3 = document.createElement('div');
    var div4 = document.createElement('div');
    div1.className = 'course-box';
    div2.className = 'course-cal pinned';
    div3.className = 'course-content';
    div4.className = 'location';

    var startPosition = 100 * (startTime - CALENDAR_START) / CALENDAR_RANGE;
    var height = 100 * duration / CALENDAR_RANGE;

    div1.style.top = startPosition + '%';
    div1.style.height = height + '%';
    div2.style.backgroundColor = 'red';
    div2.style.borderColor = 'red';

    div3.innerText = code;
    div4.innerText = location;

    div2.appendChild(div3);
    div2.appendChild(div4);
    div1.appendChild(div2);

    document.getElementsByClassName('week-day-body-col')[day].appendChild(div1);
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

