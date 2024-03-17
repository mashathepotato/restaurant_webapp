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


document.addEventListener('DOMContentLoaded', function() {

    // Add dish event listener
    const addDishForm = document.querySelector('#add-dish-form');
    if (addDishForm) {
        addDishForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addDish();
        });
    }
});

function addDish() {
    const form = document.querySelector('#add-dish-form');
    const formData = new FormData(form);
    const restaurantIdSlug = form.getAttribute('data-restaurant-id'); 

    fetch(`/ajax/add_dish/${restaurantIdSlug}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest', 
        },
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            //  has appended the new dish to the list
            const dishesList = document.querySelector('#dishes-list');
            const newDishElement = document.createElement('div');
            newDishElement.id = `dish-${data.id}`;
            newDishElement.innerHTML = `Name: ${data.name}, Price: ${data.price} <button class="delete-dish-button" data-dish-id="${data.id}">Delete</button>`;
            
            // Add event listener to the new delete button
            newDishElement.querySelector('.delete-dish-button').addEventListener('click', function() {
                deleteDish(data.id);
            });

            dishesList.appendChild(newDishElement);
            form.reset(); // Reset form fields after successful submission
        } else {
            alert("Error: Couldn't add the dish.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
