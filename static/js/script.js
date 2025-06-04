document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });

    function addToCart(productId) {
        fetch('/add-to-cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'product_id': productId,
                'quantity': 1
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // alert('Product added to cart!');
                console.log('Product added!');
            } else {
                alert('Failed to add product to cart.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});




