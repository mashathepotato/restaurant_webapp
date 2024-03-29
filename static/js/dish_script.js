document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-dish-button');
    deleteButtons.forEach(button => button.addEventListener('click', function() {
        const dishId = this.getAttribute('data-dish-id');
        deleteDish(dishId);
    }));

    const addDishForm = document.querySelector('#add-dish-form');
    if (addDishForm) {
        addDishForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addDish(this);
        });
    }
});

function deleteDish(dishId) {
    fetch(`/food_advisor/ajax/delete_dish/${dishId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', 
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

function addDish(form) {
    const formData = new FormData(form);
    const restaurantId = form.getAttribute('data-restaurant-id');
    formData.append('restaurant', restaurantId); 

    fetch(`/food_advisor/ajax/add_dish/${restaurantId}/`, {
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
            const dishesList = document.querySelector('#dishes-list');
            const newDishElement = document.createElement('div'); // could be a problem
            newDishElement.id = `dish-${data.id}`;
            newDishElement.className = "alert alert-secondary d-flex justify-content-between align-items-center mt-2";
            newDishElement.innerHTML = `Name: ${data.name}, Price: ${data.price} <button class="btn btn-danger delete-dish-button" data-dish-id="${data.id}">Delete</button>`;
            
            newDishElement.querySelector('.delete-dish-button').addEventListener('click', function() {
                deleteDish(data.id);
            });

            dishesList.appendChild(newDishElement);
            form.reset(); 
        } else {
            alert("Error: Couldn't add the dish.");
        }
    })
    .catch(error => {
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
