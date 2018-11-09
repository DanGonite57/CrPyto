$(document).ready(function () {
  $("input[name$=Sub]").on('input', function (event) {
    $.ajax({
      url: "subInputs",
      type: "POST",
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify({
        "name": this.name,
        "val": this.value,
        "ciph": document.getElementById("ciphInput").value,
        "plain": document.getElementById("plainInput").value
      }),
      success: function (json) {
        document.getElementById("plainInput").value = json["plain"]
        expandTextarea(document.getElementById("plainInput"))
        expandTextarea(document.getElementById("ciphInput"))
      }
    });
  });
});
