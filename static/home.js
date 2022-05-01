$(document).ready(function () {
    console.log("home")
    $("#start").click(function (event){
        window.location = "/lesson"
    })

    $("#quiz").click(function (event){
        window.location = "/assessment_start"
    })
});