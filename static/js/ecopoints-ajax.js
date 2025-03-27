$(document).ready(function () {
  $('#like_btn').click(function () {
    const button = $(this);
    const url = button.attr('data-url');
    const liked = button.attr('data-liked') === 'true';
    const csrftoken = getCookie('csrftoken');

    if (!liked) {
      // Like the category
      $.post({
        url: url,
        headers: {
          'X-CSRFToken': csrftoken
        },
        success: function (data) {
          $('#like_count').text(data + ' Likes');
          button.attr('data-liked', 'true');
          button.html('Liked');
        }
      });
    } else {
      // Unlike the category
      $.ajax({
        url: url,
        headers: {
          'X-CSRFToken': csrftoken
        },
        type: 'DELETE',
        success: function (data) {
          $('#like_count').text(data + ' Likes');
          button.attr('data-liked', 'false');
          button.html('Like');
        }
      });
    }
  });
});


// from django docs
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
