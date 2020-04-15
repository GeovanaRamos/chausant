$(document).ready(function () {
	var token = Cookies.get('csrftoken');
    var postData = { csrfmiddlewaretoken: token };
    $(document).on( 'click' , ".delete" , function(e) {
      e.preventDefault();
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