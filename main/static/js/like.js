document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.btn-addwish-b2');
    const removeButtons = document.querySelectorAll('.remove-liked-product');
    const heartIconLink = document.querySelector('a.icon-header-item.cl2.hov-cl1.trans-04.icon-header-noti');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const productId = this.getAttribute('data-product-id');

            fetch(`/like/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'liked') {
                    this.querySelector('.icon-heart1').src = "/static/images/icons/icon-heart-02.png";
                    updateHeartIconCount(1); // Update data-notify +1
                } else if (data.status === 'unliked') {
                    this.querySelector('.icon-heart1').src = "/static/images/icons/icon-heart-01.png";
                    updateHeartIconCount(-1); // Update data-notify -1
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    removeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const productId = this.getAttribute('data-product-id');

            fetch(`/like/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'unliked') {
                    window.location.reload(); // Refresh the page
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    function updateHeartIconCount(change) {
        let currentCount = parseInt(heartIconLink.getAttribute('data-notify')) || 0;
        currentCount += change;
        heartIconLink.setAttribute('data-notify', currentCount);

        // Optionally, toggle visibility based on count
        if (currentCount > 0) {
            heartIconLink.classList.add('icon-header-noti');
        } else {
            heartIconLink.classList.remove('icon-header-noti');
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});





