

/*fucntion in tab2*/
/* function using to demonstrate changing the html content--> */

$(function () {
    $(':input#DOM1_but').click(function () {
        document.getElementById("DOM1_p").innerHTML="I am changed!";
    }
    )
})


/* function using to demonstrate changing the CSS style--> */
$(function () {
    $(':input#DOM2_but').click(function () {
        document.getElementById("DOM2_p2").style.color="blue";
        document.getElementById("DOM2_p2").style.fontFamily="Arial";
        document.getElementById("DOM2_p2").style.fontSize="larger";
    }
    )
})

/* function using to demonstrate create a new HTML element--> */
$(function () {
    $(':input#DOM3_but').click(function () {
        var para=document.createElement("p");
        var node=document.createTextNode("I am a new text!");
        para.appendChild(node);

        var element=document.getElementById("div_create");
        element.appendChild(para);
    }
    )
})

/*fucntion in tab4*/
/*show the date with clicking the button*/
function displayDate()
{
document.getElementById("JS_event_but1_p").innerHTML=Date();
}

/*Upper the letter after input*/
function upperletter()
{
var x=document.getElementById("JS_event_input1");
x.value=x.value.toUpperCase();
}

/*change element with mouse over and out*/
function mOver(obj)
{
document.getElementById("JS_event_mousover").innerHTML="thank you"
}

function mOut(obj)
{
document.getElementById("JS_event_mousover").innerHTML="hover your mouse on me"
}


/* function using ajax to import COVID19 data--> */

$(function () {
    $(':input#showCOVID').click(function () {
        $.ajax({
            url: 'https://coronavirus-tracker-api.herokuapp.com/v2/locations',
            type: 'get',
            dataType: 'json',
            success: function (d) {
                var datas = d.locations
                var tbhtml = "<tr><th>country</th><th>province</th><th>confirmed</th><th>deaths</th><th>recovered</th><th>updatetime</th></tr>";
                for (var i = 0; i < datas.length; i++) {
                    tbhtml += "<tr><td>" + datas[i].country + "</td><td>" + datas[i].province + "</td><td>" + datas[i].latest.confirmed + "</td><td>" + datas[i].latest.deaths + "</td><td>" + datas[i].latest.recovered + "</td><td>" + datas[i].last_updated + "</td></tr>";
                }

                $('table#COVIDtable').html(tbhtml);
            }
        })
    })
})

$(function () {
    $(':input#clean').click(function () {
        var tbhtml = "<tr><th>country</th><th>province</th><th>confirmed</th><th>deaths</th><th>recovered</th><th>updatetime</th></tr>";
        $('table#COVIDtable').html(tbhtml);
    })
})

/* back up if the api crashed*/
$(function () {
    $(':input#showCOVID_b').click(function () {
        $.ajax({
            url: 'datas.json',
            type: 'get',
            dataType: 'json',
            success: function (d) {
                var datas = d.locations
                var tbhtml = "<tr><th>country</th><th>province</th><th>confirmed</th><th>deaths</th><th>recovered</th><th>updatetime</th></tr>";
                for (var i = 0; i < datas.length; i++) {
                    tbhtml += "<tr><td>" + datas[i].country + "</td><td>" + datas[i].province + "</td><td>" + datas[i].latest.confirmed + "</td><td>" + datas[i].latest.deaths + "</td><td>" + datas[i].latest.recovered + "</td><td>" + datas[i].last_updated + "</td></tr>";
                }

                $('table#COVIDtable_b').html(tbhtml);
            }
        })
    })
})

$(function () {
    $(':input#clean_b').click(function () {
        var tbhtml = "<tr><th>country</th><th>province</th><th>confirmed</th><th>deaths</th><th>recovered</th><th>updatetime</th></tr>";
        $('table#COVIDtable_b').html(tbhtml);
    })
})


/* if else*/

function checknumber(){
    if(txt_Number.value%2==0){
        alert("this is an even");
    }else
        alert("this is an odd");
}

/* for */

function numberadds() {
    var text = "";
    var i;
    for (i = 0; i < 5; i++) {
        text += "The number is " + i + "<br>";
    }
    document.getElementById("foriter").innerHTML = text;
}