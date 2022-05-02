$(document).ready(function () {
  $("#slider-output").hide();
  $("#setting").text(images[0][1]);
  $("#image").attr("src", images[0][0]);

  $("#slider").on("input change", function () {
    updateView();
  });

  $("#next").click(function () {
    window.location.href = "/lesson";
  });

  $("#lesson").click(function () {
    window.location.href = "/lesson/" + lesson_topic;
  });
});

function updateView() {
  let num = $("#slider-output").text();
  $("#image").attr("src", images[num][0]);
  $("#setting").text(images[num][1]);
}
