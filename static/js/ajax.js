var isLoading = false;
$(document).on("submit", "form.ajax", function (e) {
    console.log('===================')
    e.preventDefault();
    var $this = $(this),
        data = new FormData(this),
        action_url = $this.attr("action"),
        reset = $this.hasClass("reset"),
        reload = $this.hasClass("reload"),
        redirect = $this.hasClass("redirect"),
        redirect_url = $this.attr("data-redirect");

    if (!isLoading) {
        isLoading = true;
        $.ajax({
            url: action_url,
            type: "POST",
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            dataType: "json",
            success: function (data) {
                var status = data.status;
                var title = data.title;
                var message = data.message;
                var pk = data.pk;
                if (status == "true") {
                    title ? (title = title) : (title = "Success");
                    Swal.fire({
                        title: title,
                        html: message,
                        icon: "success",
                    }).then(function () {
                        redirect && (window.location.href = redirect_url), reload && window.location.reload(), reset && window.location.reset();
                    });
                } else {
                    title ? (title = title) : (title = "An Error Occurred");
                    Swal.fire({
                        title: title,
                        html: message,
                        icon: "error",
                    });
                }
            },
            error: function (data) {
                var title = "An error occurred",
                    message = "something went wrong";
                Swal.fire({
                    title: title,
                    html: message,
                    icon: "error",
                });
            },
        }).then(function (response) {
            isLoading = false;
        });
    }
});



$(document).ready(function() {
    $('.btn-wishlist').click(function(e) {
        e.preventDefault();
        var storeId = $(this).data('store-id');
        var wishlistUrl = $(this).data('wishlist-url');
        var button = $(this);

        $.ajax({
            type: 'GET',
            url: wishlistUrl, // URL to add/remove from wishlist
            success: function(data) {
                if (data.wished) {
                    // Item was added to wishlist
                    button.find('i').removeClass('fa-regular').addClass('fa-solid').css('color', '#ff0000');
                    button.attr('title', 'Remove from Wishlist');
                           
                } else {
                    // Item was removed from wishlist
                    button.find('i').removeClass('fa-solid').addClass('fa-regular').css('color', '#001d42');
                    button.attr('title', 'Add to Wishlist');
                }

                // Update wishlist count on both pages
                var currentCount = parseInt($('.wishlist-count').text());
                if (data.wished) {
                    // If item was added, increment count
                    $('.wishlist-count').text(currentCount + 1);
                } else {
                    // If item was removed, decrement count
                    $('.wishlist-count').text(currentCount - 1);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                // Handle error
            }
        });
    });
});
$(document).ready(function() {
    $('.btn-wishlist').click(function(e) {
      e.preventDefault();
      var storeId = $(this).data('store-id');
      var button = $(this); // Store the button reference for later use
      $.ajax({
        type: 'GET',
        url: '/add_to_wishlist/' + storeId + '/',
        dataType: 'json',
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
        },
        success: function(data) {
          console.log(data); // Check if 'wished' is present and holds the correct value
          $('.wishlist_num_count').text(data.wishlist_count);
          // Handle success, update UI based on 'data' response
          if (data.wished) {
            // Item was added to wishlist
            button.find('i').removeClass('fa-regular').addClass('fa-solid').css('color', '#ff0000');
            button.attr('title', 'Remove from Wishlist');
          } else {
            // Item was removed from wishlist
            button.find('i').removeClass('fa-solid').addClass('fa-regular').css('color', '#001d42');
            button.attr('title', 'Add to Wishlist');
          }
        },
        error: function(xhr, textStatus, errorThrown) {
          // Handle error
        }
      });
    });
  });