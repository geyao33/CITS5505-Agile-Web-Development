var multipleAnswer = function (rightans, span, options) {
    var spanname = document.getElementById(span)
    var opt = document.getElementsByName(options)

    for (i = 0; i < opt.length; i++) {
        if (opt[i].checked) {
            valuer = opt[i].value
        } else { spanname.innerHTML = '<h4>Please pick an option<h4>' }
    }

    var choop = document.getElementById(valuer);


    if (valuer == rightans) {
        spanname.innerHTML = '<h4> Yes, you chose right answer! </h4>';
        choop.style.border = '3px solid limegreen';
    } else {
        spanname.innerHTML = '<h4> Wrong, the right answer is ' + rightans + '</h4>';
        choop.style.border = '3px solid red';
    }

}

var calAnswer = function (rightans, span, numQue) {
    var spanname = document.getElementById(span)
    var Que = document.getElementById(numQue)

    if (Que.value == "") {
        spanname.innerHTML = '<h4>Please enter your answer<h4>'
    } else {
        if (Que.value == rightans) {
            spanname.innerHTML = "<h4> Your answer is right! </h4>"
            Que.style.border = '3px solid limegreen';
        } else {
            spanname.innerHTML = '<h4> Wrong, the right answer is ' + rightans + '</h4>';
            Que.style.border = '3px solid red';
        }
    }
}