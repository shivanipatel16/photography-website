$(document).ready(function () {

$('#startbutton').click(function () {
    if (currq > 0) {
        window.location.href = `/assessment/${currq}`;
    }
    else {
        window.location.href = "/assessment/1";
    }
});
});