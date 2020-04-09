$(document).ready(function () {
	var token = Cookies.get('csrftoken');
    var postData = { csrfmiddlewaretoken: token };
    $(".delete").click(function () {
      $.ajax({
        method: 'POST',
        url: $(this).attr("data-href"),
        data: postData,
        success: function (response) {
          window.location.reload();
        },
      });
    });
});