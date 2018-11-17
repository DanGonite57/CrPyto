$(document).ready(function () {
  $('#submitBtn').prop('disabled', true);
  $('#ciphInput').keyup(function () {
    $('#submitBtn').prop('disabled', this.value == "" ? true : false);
  })
});
