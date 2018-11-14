$(document).ready(function () {
  $("#spaceBtn").on('click', function (event) {
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
        expandTextarea(document.getElementById("ciphInput"))
      }
    });
  });
});
