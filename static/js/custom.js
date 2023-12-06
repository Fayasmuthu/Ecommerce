$('.range-slider-value-min, .range-slider-value-max').on('input', function() {
    var minPrice = $('#min-price').val();
    var maxPrice = $('#max-price').val();

    $.ajax({
        type: 'GET',
        url: '/filter-products-by-price/',  // Replace with your Django view URL
        data: {
            'min_price': minPrice,
            'max_price': maxPrice
        },
        success: function(response) {
            // Update the product list or container with the filtered data received in the response
            $('.product-list-container').html(response.data);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
});
