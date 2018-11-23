function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


//Tue: 9:00-10:15   startTimeDiff = startTime-8:00
//addClass(2, 60, 75, name, location)
function addClass(day, startTimeDiff, timeSpan, name, location){
    var div1 = document.createElement('div');
    var div2 = document.createElement('div');
    var div3 = document.createElement('div');
    var div4 = document.createElement('div');

    div1.className = 'course-box';
    div2.className = 'course-cal pinned';
    div3.className = 'course-content';
    div4.className = 'location';

    //compute time
    var startTimePosition = startTimeDiff*75/600;
    var height = timeSpan*75/600;

    div1.style.top = startTimePosition+'%';
    div1.style.height = height+'%';
    div2.style.backgroundColor = 'red';
    div2.style.borderColor = 'red';


    div3.innerText = name;
    div4.innerText = location;

    div2.appendChild(div3);
    div2.appendChild(div4);
    div1.appendChild(div2);

    document.getElementsByClassName('wk-day-body')[day].appendChild(div1);
 
}




// <div class="course-box" style="top: 10%; height: 5.95238%;">
//     <div class="course-cal pinned" style="background-color: rgb(242, 121, 218); border-color: rgb(242, 121, 218);">
//         <div class="course-content">ARBC - 1002</div>
//         <div class="location">Engr Science &amp; Mech G8</div>
//     </div>
// </div>