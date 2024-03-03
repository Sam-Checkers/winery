function addToShelf(wine_id, user_id) {
    $.ajax({
        type: 'POST',
        url: '/add_to_shelf',
        data: {
            user_id: user_id,
            wine_id: wine_id,
        },
        success: function(response) {
            alert(response.message);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function removeFromShelf(wine_id, user_id) {
    $.ajax({
        type: 'POST',
        url: '/remove_from_shelf',
        data: {
            user_id: user_id,
            item_id: wine_id
        },
        success: function(response) {
            alert(response.message);
            updateCartItems(user_id);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$('.add-to-shelf').on('click', function() {
    var wine_id = $(this).data('wine-id');
    var user_id = 123;
    addToShelf(wine_id, user_id);
});