$(document).ready(function () {
	$("#splitBtn").on('click', function (event) {
		$.ajax({
			url: "splitKey",
			type: "POST",
			contentType: "application/json",
			dataType: "json",
			data: JSON.stringify({
				"key": document.getElementById("keyInput").value
			}),
			success: function (json) {
				document.getElementById("keyInput").value = json["key"]
			}
		});
	});
});
