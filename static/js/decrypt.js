$(document).ready(function () {
  $("submitBtn").on('click', function (event) {
    $.ajax({
      url: "decrypt",
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({
        "cipher": document.title,
        "ciph": document.getElementById("ciphInput").value,
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
