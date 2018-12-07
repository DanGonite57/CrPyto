$(document).ready(function () {
  $("#addSpaceBtn").on('click', function (event) {
    $.ajax({
      url: "addSpaces",
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({
        "plain": document.getElementById("plainInput").value
      }),
      success: function (json) {
        document.getElementById("plainInput").value = json["plain"]
        document.getElementById("scoreLbl").innerHTML = json["score"]
        expandTextarea(document.getElementById("plainInput"))
      }
    });
  });
  $("#remSpaceBtn").on('click', function (event) {
    $.ajax({
      url: "remSpaces",
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({
        "plain": document.getElementById("plainInput").value
      }),
      success: function (json) {
        document.getElementById("plainInput").value = json["plain"]
        document.getElementById("scoreLbl").innerHTML = json["score"]
        expandTextarea(document.getElementById("plainInput"))
      }
    });
  });
  $("#remPuncBtn").on('click', function (event) {
    $.ajax({
      url: "remPunc",
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({
        "plain": document.getElementById("plainInput").value
      }),
      success: function (json) {
        document.getElementById("plainInput").value = json["plain"]
        document.getElementById("scoreLbl").innerHTML = json["score"]
        expandTextarea(document.getElementById("plainInput"))
      }
    });
  });
});
