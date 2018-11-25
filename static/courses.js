var CALENDAR_START = 480 // 8:00 AM in minutes
var CALENDAR_END = 1320 // 10:00 PM in minutes
var CALENDAR_RANGE = CALENDAR_END - CALENDAR_START
var DAYS_ENUM = Object.freeze({'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4})

/**
 * Converts times into military time minutes; for use with course addition.
 * 
 * @param {*} time - string in the form '4:30 pm' or '5:30 am'
 */
function parseTime(time) {
    var time = time.trim()
    var colon_index = time.indexOf(":")
    var timeType = time.substring(colon_index + 4)
    var hours = parseInt(time.substring(0, colon_index))
    var minutes = parseInt(time.substring(colon_index + 1, colon_index + 3))
    if (timeType === 'pm') {
        hours += 12
    }
    return (60 * hours) + minutes
}

/**
 * Converts day strings into arrays of indices to use on the calendar.
 * 
 * @param {*} days - string in the form 'MTWRF'
 */
function parseDays(days) {
    var indices = []
    for (var i = 0; i < days.length; i++) {
        indices.push(DAYS_ENUM[days.charAt(i)])
    }
    return indices
}

function getSubjects() {
    db.ref('subjects').once('value').then(function(snapshot) {
        window.SUBJECTS = Object.keys(snapshot.val())
        window.subjnames = snapshot.val()
    });
}

function showSubjects() {
    var subjectList = document.getElementById('subject-list')
    var courseList = document.getElementById('course-list')
    for (var i = 0; !ALREADY_POPULATED && i < SUBJECTS.length; i++) {
        var subjectName = window.subjnames[SUBJECTS[i]]
        var element = document.createElement('a')
        element.textContent = SUBJECTS[i] + ' - ' + subjectName
        element.setAttribute('onclick', "getCoursesDropdown(\'" + SUBJECTS[i] + "\')")
        subjectList.appendChild(element)
    }

    if (courseList.className === 'dropdown-content show') {
        courseList.classList.toggle('show')
    }
    subjectList.classList.toggle('show')
    ALREADY_POPULATED = true
}

function filterSubjects() {
    var input = document.getElementById("search-subject");
    var filter = input.value.toUpperCase();
    var div = document.getElementById("subject-list");
    var a = div.getElementsByTagName("a");
    for (var i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function getCoursesDropdown(subject) {
    var subjectList = document.getElementById('subject-list')
    var courseDropdown = document.getElementById('course-dropdown')
    var courseList = document.getElementById('course-list')
    db.ref('courses_by_abbr').child(subject).once('value').then(function(snapshot) {
        window.abbrData = snapshot.val()
        while (courseList.firstChild) {
            courseList.removeChild(courseList.firstChild)
        }
        var searchInput = document.createElement('input')
        searchInput.type = 'text'
        searchInput.setAttribute('id', 'search-course')
        searchInput.setAttribute('onkeyup', 'filterCourses()')
        courseList.appendChild(searchInput)

        var courses = Object.keys(abbrData)
        for (var i = 0; i < courses.length; i++) {
            var course = String(courses[i])
            var identifier = abbrData[course]['identifier']
            var name = abbrData[course]['name']
            for (var j = 0; j < identifier.length; j++) {
                if (!isNaN(identifier.charAt(j))) {
                    identifier = identifier.substring(j).trim()
                    break
                }
            }
            var element = document.createElement('a')
            var functionCall = "getCourseSections(\'" + course + "\')"
            element.textContent = identifier + ' - ' + name
            element.setAttribute('onclick', functionCall)
            courseList.appendChild(element)
        }
        courseDropdown.style = ''
        subjectList.classList.toggle('show')
    });
}

function showCourses() {
    var courseList = document.getElementById('course-list')
    courseList.classList.toggle('show')
}

function filterCourses() {
    var input = document.getElementById("search-course");
    var filter = input.value.toUpperCase();
    var div = document.getElementById("course-list");
    var a = div.getElementsByTagName("a");
    for (var i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

function getCourseSections(course) {
    var courseSections = document.getElementById('course-sections')
    while (courseSections.firstChild) {
        courseSections.removeChild(courseSections.firstChild)
    }
    var courseList = document.getElementById('course-list')

    var sectionTable = document.createElement('table')
    sectionTable.style.width = '100%'
    sectionTable.style.border = '1px solid black'

    var courseData = abbrData[course]
    var sections = courseData['sections']
    for (var i = 0; i < sections.length; i++) {
        var tr = sectionTable.insertRow()
        var section = sections[i]
        var instructor = section['instructors'][0]
        var td = document.createElement('td')
        td.appendChild(document.createTextNode(instructor))
        tr.appendChild(td)
        var td1 = document.createElement('td')
        td1.appendChild(document.createTextNode(section['section_id']))
        tr.appendChild(td1)
        var meetings = section['meetings']
        for (var j = 0; j < meetings.length; j++) {
            var meeting = meetings[j]
            var td2 = document.createElement('td')
            td2.appendChild(document.createTextNode(meeting['days']))
            tr.appendChild(td2)
            var days = parseDays(meeting['days'])
            var location = section['location']
            var rawTime = meeting['time']
            var rawTimeDelimiter = rawTime.indexOf('-')
            var startTime = parseTime(rawTime.substring(0, rawTimeDelimiter).trim())
            var endTime = parseTime(rawTime.substring(rawTimeDelimiter + 1).trim())
            var duration = endTime - startTime
        }
        courseSections.appendChild(tr)
    }
    courseSections.style.display = 'block'
    courseList.classList.toggle('show')
}

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

    // TODO: Add randomized colors for course bubbles (don't repeat).

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

window.onload = function() {
    window.courses = []
    window.db = initDB()
    window.ALREADY_POPULATED = false
    getSubjects()
}