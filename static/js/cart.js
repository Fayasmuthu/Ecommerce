
    $('.add-to-cart-btn').click(function(event) {
        event.preventDefault();
        var productId = $(this).data('product-id');
        
        $.ajax({
            type: 'POST',
            url: '{% url "order:cart_add" 0 %}'.replace('0', productId),
            dataType: 'json',
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
            },
            success: function(data) {
                // Update cart icon count or total amount displayed on the page
                $('.cart_num_count').text(data.cart_count);
                $('.cart-total-amount').text('$' + data.cart_total_amount);
                // Call showAlert function with appropriate parameters
                // showAlert('Cart updated successfully!', 'alert-success');
                showAlert(data.message, "alert-success");
            },
            error: function(xhr, errmsg, err) {
                console.log(errmsg);
                // Call showAlert function for error handling
                if (data.status == '401') {window.location.href = '/accounts/login/';
                showAlert('Error updating cart. Please try again.', 'alert-danger');
                                  // Show a custom message
            }  
            }
        });
    });
    function showAlert(message, alertClass) {
      var alertContainer = $("#alert-container");
      var alertDiv = $("<div>").addClass("alert " + alertClass).text(message);
      alertContainer.append(alertDiv);

      // Automatically hide the alert after 5 seconds
      setTimeout(function () {
          alertDiv.remove();
      }, 800);
  }

