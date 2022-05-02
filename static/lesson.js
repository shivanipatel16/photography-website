$(document).ready(function () {
    if (iso_visit > 0) {
        $("#learn_iso_inter").prop("disabled", false)
        $("#learn_iso_inter").css({color: 'default'})
        $("#learn_iso_inter").addClass("hover")
    }
    else {
        $("#learn_iso_inter").prop("disabled", true)
        $("#learn_iso_inter").css({color: 'lightgrey'})
    }
    if (ape_visit > 0) {
        $("#learn_aper_inter").prop("disabled", false)
        $("#learn_aper_inter").css({color: 'default'})
        $("#learn_aper_inter").addClass("hover")
    }
    else {
        $("#learn_aper_inter").prop("disabled", true)
        $("#learn_aper_inter").css({color: 'lightgrey'})
    }
    if (spd_visit > 0) {
        $("#learn_ss_inter").prop("disabled", false)
        $("#learn_ss_inter").css({color: 'default'})
        $("#learn_ss_inter").addClass("hover")
    }
    else {
        $("#learn_ss_inter").prop("disabled", true)
        $("#learn_ss_inter").css({color: 'lightgrey'})
    }

    if (iso_visit > 0 && ape_visit > 0 && spd_visit >0){
        console.log("print")
        $("#quiz-finished").text("You finished the material! Take the quiz now.")
    }

    $("#quiz").click(function (event) {
        if (currq > 0) {
            window.location = `/assessment/${currq}`
        }
        else {
            window.location = "/assessment_start"
        }
    })

    $("#learn_iso").click(function (event) {
        window.location = "/lesson/iso"
    })

    $("#learn_aper").click(function (event) {
        window.location = "/lesson/aperture"
    })

    $("#learn_ss").click(function (event) {
        window.location = "/lesson/shutter_speed"
    })

    $("#learn_iso_inter").click(function (event) {
        window.location = "/lesson/interactive/iso"
    })

    $("#learn_aper_inter").click(function (event) {
        window.location = "/lesson/interactive/aperture"
    })

    $("#learn_ss_inter").click(function (event) {
        window.location = "/lesson/interactive/shutter_speed"
    })

});
