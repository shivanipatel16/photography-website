$(document).ready(function () {
    $('#nextlesson').click(function () {
        window.location.href = "/lesson/interactive/" + lesson_topic;
    });
});