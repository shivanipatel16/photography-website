function update_userscore(correct_tally) {
  let data_to_add = correct_tally;
  $.ajax({
    type: "POST",
    url: "/update_userscore",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data_to_add),
    success: function (result) {},
    error: function (request, status, error) {
      console.log("Error");
      console.log(request);
      console.log(status);
      console.log(error);
    },
  });
}

function review_currquestion(currq) {
  let data_to_add = currq;
  $.ajax({
    type: "POST",
    url: "/review_currquestion",
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data_to_add),
    success: function (result) {},
    error: function (request, status, error) {
      console.log("Error");
      console.log(request);
      console.log(status);
      console.log(error);
    },
  });
}

$(document).ready(function () {
  let correct_tally = -1;
  console.log("currq: " + currq);

  $("#nextbutton").click(function () {
    if (correct_tally == -1) {
      console.log("nothing selected");
    } else {
      window.location.href = "/assessment/" + nextq;
    }
  });

  if (currq == 9) {
    $("#nextbutton").click(function () {
      if (correct_tally == -1) {
        console.log("nothing selected");
      } else {
        window.location.href = "/assessment_complete";
      }
    });
  }

  $('input[name="test"]').click(function () {
    let user_ans = $(this).val();
    if (user_ans == correct_ans) {
      correct_tally = 1;
      update_userscore(correct_tally);
    } else {
      correct_tally = 0;
      update_userscore(correct_tally);
    }
    $(".pop_up").dialog("close");
  });

  $("#correctexplan").dialog({
    autoOpen: false,
  });

  $("#confirmation").dialog({
    autoOpen: false,
  });

  $("#submitbutton").click(function () {
    if (correct_tally == 0) {
      $("#correctexplan").dialog("open");
    } else if (correct_tally == 1) {
      $("#confirmation").dialog("open");
    }
  });

  $(".okbtn").click(function () {
    $("#correctexplan").dialog("close");
  });

  $(".okbtn").click(function () {
    $("#confirmation").dialog("close");
  });

  $("#reviewbutton").click(function () {
    review_currquestion(currq);
    window.location.href = "/lesson";
  });
});
