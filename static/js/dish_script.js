// static/js/dish_script.js

document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-dish-button');
    deleteButtons.forEach(button => button.addEventListener('click', function() {
        const dishId = this.getAttribute('data-dish-id');
        deleteDish(dishId);
    }));
});

function deleteDish(dishId) {
    fetch(`/ajax/delete_dish/${dishId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            document.getElementById(`dish-${dishId}`).remove();
        } else {
            alert("Error: Couldn't delete the dish.");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
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
