/*----------------------------------------------
Note: All functions are called from forms.py
----------------------------------------------*/

//  Enable/Disable 'PROFESSIONAL CARD'. [X] I have experience

$(document).ready(function() {
    $(function() {
        Emp();
        $("#emp").click(Emp);
    });
    function Emp() {
        if (this.checked) {
            $("input.emp, textarea.emp").removeAttr("disabled")
        }
        else {
            $("input.emp, textarea.emp").attr("disabled", true)
        }
    }   
});

// 2) Enable/Disable 'FINISHED DATE (Card professional)'.
// [X] I am employed = Disable

$(function() {
    Exp();
    $("#exp").click(Exp);
});
function Exp() {
    if (this.checked) {
        $("input#go").attr("disabled", true);
        $("#go").val("");  //Clear to prevent sending data
    }
    else {
        $("input#go").removeAttr("disabled");
    }   
}


// Enable/Disable 'FINISHED DATE (Card educational)'.
// if status course is 'Completed', enable the finished input date
// Pure JS
function statusCourse(edu){
    var x =document.getElementsByName("finished_course");
    for(var j = 0; j < x.length; j++) {
        x[j].disabled =! (edu.value == "Completed")
        x[j].value = '';
    }
}
    

