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
    if (timeType === 'pm' && hours != 12) {
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
            if (!abbrData[course].hasOwnProperty('sections')) continue

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

function testHover(event){
    console.log('Hover!!')
    
    //el.setAttribute('on', 'true')
}

function getCourseSections(course) {
    var courseSections = document.getElementById('course-sections')
    while (courseSections.firstChild) {
        courseSections.removeChild(courseSections.firstChild)
    }
    var courseList = document.getElementById('course-list')

    var sectionTable = document.createElement('table')
    sectionTable.setAttribute('class', 'table table-hover')


    // var thread = document.createElement('thread')
    // var trHead = document.createElement('tr')
    // var th = document.createElement('th')
    // th.appendChild(document.createTextNode('CRN'))
    // trHead.appendChild(th)
    // th = document.createElement('th')
    // th.appendChild(document.createTextNode('Instructor'))
    // trHead.appendChild(th)
    // th = document.createElement('th')
    // th.appendChild(document.createTextNode('Section'))
    // trHead.appendChild(th)
    // thread.appendChild(trHead)
    // sectionTable.appendChild(thread)
    // sectionTable.appendChild(document.createTextNode('<thead> \
    //                                                     <tr> \
    //                                                       <th>CRN</th> \
    //                                                       <th>Instructor</th> \
    //                                                       <th>Section</th> \
    //                                                     </tr> \
    //                                                   </thead>'))

    var tbody = document.createElement('tbody')
    //tbody.setAttribute('style', 'overflow-y:auto;')

    var courseData = abbrData[course]
    var sections = courseData['sections']
    window.crn2courseData = {}



    for (var i = 0; i < sections.length; i++) {
        var tr = document.createElement('tr')
        //tr.setAttribute('onmouseover', 'testHover()')
        var section = sections[i]

        var td = document.createElement('td')
        td.appendChild(document.createTextNode(section['crn']))
        tr.appendChild(td)

        var instructor = 'To Be Announced'
        if (section.hasOwnProperty('instructors')){
            for (var j = 0; j < section['instructors'].length; j++){
                if (section['instructors'][j].length > 0){
                    instructor = section['instructors'][j]
                    break
                }
            }
        }

        var td1 = document.createElement('td')
        td1.appendChild(document.createTextNode(instructor))
        tr.appendChild(td1)

        var td2 = document.createElement('td')
        td2.appendChild(document.createTextNode(section['section_id']))
        tr.appendChild(td2)

        var meeting_obj = []
        console.log(section)
        if (section.hasOwnProperty('meetings') && section['meetings'].length != 0){
            var meetings = section['meetings']

            for (var j = 0; j < meetings.length; j++) {
                var meeting = meetings[j]

                if (!meeting.hasOwnProperty('days') || !meeting.hasOwnProperty('time')){
                    console.log('Day and time to be announced.')
                    continue
                }
                var days = parseDays(meeting['days'])
                var rawTime = meeting['time']
                var rawTimeDelimiter = rawTime.indexOf('-')
                var startTime = parseTime(rawTime.substring(0, rawTimeDelimiter).trim())
                var endTime = parseTime(rawTime.substring(rawTimeDelimiter + 1).trim())
                var duration = endTime - startTime

                if (!meeting.hasOwnProperty('location')){
                    var location = 'To Be Announced'
                }else{
                    var location = meeting['location']
                }

                meeting_obj.push({  days: days,
                                    startTime: startTime,
                                    duration: duration,
                                    location: location})
            }
            //tr.setAttribute('onclick', '')
        }

        window.crn2courseData[section['crn']] = {courseInfo: courseData,
                                                 meeting_obj: meeting_obj}
        tr.setAttribute('onclick', 'register("' + section['crn'] + '", "' + course + '")')
        //courseSections.appendChild(tr)
        console.log(crn2courseData)
        tbody.appendChild(tr)
    }
    sectionTable.appendChild(tbody)
    courseSections.appendChild(sectionTable)
    $('.table').bootstrapTable('refresh')

    courseSections.style.display = 'block'
    courseList.classList.toggle('show')
    //console.log(window.crn2courseData)
}

function register(crn, code){

    if (!window.schedule.hasOwnProperty(crn)){
        window.schedule[crn] = []
        window.schedule[crn].push(addDropdownSection(crn))
        meeting_obj = window.crn2courseData[crn]['meeting_obj']
        var color = 'rgb(' + (Math.floor(Math.random() * 256)) + ',' + (Math.floor(Math.random() * 256)) + ',' + (Math.floor(Math.random() * 256)) + ')';
        for (var i = 0; i < meeting_obj.length; i++){
            obj = meeting_obj[i]
            for (var j = 0; j < obj['days'].length; j++){
                window.schedule[crn].push(addClass(code, obj['days'][j], obj['startTime'], obj['duration'], obj['location'], color))
            }
        }
    }
}

function unregister(crn){
    if (window.schedule.hasOwnProperty(crn)){
        for (var i = 0; i < window.schedule[crn].length; i++){
            window.schedule[crn][i].remove()
        }
        delete window.schedule[crn]
    }
}



function updateSchedule(crn, code){
    if (!window.schedule.hasOwnProperty(crn)){
        addDropdownSection(crn)
        window.schedule[crn] = []
        meeting_obj = window.crn2courseData[crn]['meeting_obj']
        var color = 'rgb(' + (Math.floor(Math.random() * 256)) + ',' + (Math.floor(Math.random() * 256)) + ',' + (Math.floor(Math.random() * 256)) + ')';
        for (var i = 0; i < meeting_obj.length; i++){
            obj = meeting_obj[i]
            for (var j = 0; j < obj['days'].length; j++){
                window.schedule[crn].push(addClass(code, obj['days'][j], obj['startTime'], obj['duration'], obj['location'], color))
            }
        }
    }else{
        for (var i = 0; i < window.schedule[crn].length; i++){
            window.schedule[crn][i].remove()
        }
        delete window.schedule[crn]
    }
}

function loadSchedule(crns){
    window.crn2courseData = {}
    for (var i = 0; i < crns.length; i++){
        getDatabyKey(window.db, 'Courses_2019_Spring', crns[i])
        .then( function (section){
            var meeting_obj = []
            if (section.hasOwnProperty('meetings') && section['meetings'].length != 0){
                var meetings = section['meetings']

                for (var j = 0; j < meetings.length; j++) {
                    var meeting = meetings[j]

                    if (!meeting.hasOwnProperty('days') || !meeting.hasOwnProperty('time')){
                        console.log('Day and time to be announced.')
                        continue
                    }
                    var days = parseDays(meeting['days'])
                    var rawTime = meeting['time']
                    var rawTimeDelimiter = rawTime.indexOf('-')
                    var startTime = parseTime(rawTime.substring(0, rawTimeDelimiter).trim())
                    var endTime = parseTime(rawTime.substring(rawTimeDelimiter + 1).trim())
                    var duration = endTime - startTime

                    if (!meeting.hasOwnProperty('location')){
                        var location = 'To Be Announced'
                    }else{
                        var location = meeting['location']
                    }

                    meeting_obj.push({  days: days,
                                        startTime: startTime,
                                        duration: duration,
                                        location: location})
                }
            }

            window.crn2courseData[section['crn']] = {courseInfo: section,
                                                     meeting_obj: meeting_obj}
            register(section['crn'], section['identifier'])
        })
    }

}

function addDropdownSection(crn){
    courseData = window.crn2courseData[crn]
    var registered = document.getElementById('accordion')

    var regSection = document.createElement('div')
    regSection.setAttribute('class', 'card')

    var headerDiv = document.createElement('div')
    headerDiv.setAttribute('class', 'card-header')
    headerDiv.setAttribute('style','height: 50px;')
    headerDiv.setAttribute('id', crn + 'heading')

    var delButton = document.createElement('button')
    delButton.setAttribute('type', 'button')
    delButton.setAttribute('class', 'close')
    delButton.setAttribute('aria-label', 'Close')
    delButton.setAttribute('onclick', 'unregister("' + crn + '")')

    var span = document.createElement('span')
    span.setAttribute('aria-hidden', 'true')
    span.innerHTML = '&times;'
    console.log(span)

    delButton.appendChild(span)
    headerDiv.appendChild(delButton)

    var button = document.createElement('button')
    button.setAttribute('class', 'btn btn-link collapsed')
    button.setAttribute('data-toggle', 'collapse')
    button.setAttribute('data-target', '#body' + crn)
    button.setAttribute('aria-expanded', 'false')
    button.setAttribute('aria-controls', 'body' + crn)
    button.setAttribute('style', 'padding: None;')
    button.appendChild(document.createTextNode(courseData['courseInfo']['fullname']))

    headerDiv.appendChild(button)
    regSection.appendChild(headerDiv)

    var bodyDiv = document.createElement('div')
    bodyDiv.setAttribute('id', 'body' + crn)
    bodyDiv.setAttribute('class', 'collapse')
    bodyDiv.setAttribute('aria-labelledby', crn + 'heading')
    bodyDiv.setAttribute('data-parent', '#accordion')

    var innerBody = document.createElement('div')
    innerBody.setAttribute('class', 'card-body')
    
    head = document.createElement('h5')
    head.appendChild(document.createTextNode('Description'))
    innerBody.appendChild(head)

    p = document.createElement('p')
    if (courseData['courseInfo'].hasOwnProperty('description')){
        p.appendChild(document.createTextNode(courseData['courseInfo']['description']))
    }else{
        p.appendChild(document.createTextNode(''))
    }
    innerBody.appendChild(p)

    bodyDiv.appendChild(innerBody)
    regSection.appendChild(bodyDiv)

    registered.appendChild(regSection)

    return regSection
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
function addClass(code, day, startTime, duration, location, color) {
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

    //remove the clicked class on calendar
    div1.onclick = function() {document.getElementsByClassName('wk-day-body')[day].removeChild(div1);};

    // TODO: Add randomized colors for course bubbles (don't repeat).

    div1.style.top = startPosition + '%';
    div1.style.height = height + '%';

    
    div2.style.backgroundColor = color;
    div2.style.borderColor = color;

    div3.innerText = code;
    div4.innerText = location;

    div2.appendChild(div3);
    div2.appendChild(div4);
    div1.appendChild(div2);

    document.getElementsByClassName('week-day-body-col')[day].appendChild(div1);

    return div1
}
