const API_URL = "http://localhost:8000/users";

function createUserElement(user) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("user-wrapper");

    const userInfo = createUserInfo(user);
    const deleteButton = createRemoveButton(user.id);

    wrapper.appendChild(userInfo);
    wrapper.appendChild(deleteButton);

    return wrapper;
}

function createUserInfo(user) {
    const userInfo = document.createElement("div");
    userInfo.classList.add("user-wrapper-infos");

    const nameDiv = document.createElement("div");
    nameDiv.textContent = `${user.first_name} ${user.last_name}`;
    nameDiv.classList.add("user-wrapper-infos-name");

    const roleDiv = document.createElement("div");
    roleDiv.textContent = user.role;
    roleDiv.classList.add("user-wrapper-infos-role");

    userInfo.appendChild(nameDiv);
    userInfo.appendChild(roleDiv);

    return userInfo;
}

function createRemoveButton(userId) {
    const removeButton = document.createElement("button");
    removeButton.classList.add("remove-button");
    removeButton.setAttribute("data-id", userId);

    const iconSpan = document.createElement("span");
    iconSpan.classList.add("material-icons");
    iconSpan.textContent = "X";

    removeButton.appendChild(iconSpan);
    removeButton.addEventListener("click", () => {
        if (confirm("Do you want to delete this user?")) {
            executeDelete(userId, removeButton);
        }
    });

    return removeButton;
}

async function executeDelete(userId, button) {
    try {
        const response = await fetch(`${API_URL}/${userId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: userId })
        });
        if (response.ok) {
            const userElement = button.closest('.user-wrapper');
            userElement.remove(); 
        } else {
            alert('Cannot delete this user');
        }
    } catch (error) {
        console.error('Błąd:', error);
        alert('Error while deleting user');
    }
}

async function sendPostRequest() {
    const userData = gatherUserData();
    console.log("Dane użytkownika do wysłania:", userData);

    if (!userData.firstName) {
        alert("First name cannot be empty.");
        return;
    
    } else if (!userData.lastName) {
        alert("Last name cannot be empty.");
        return;
    } else if (!userData.role) {
        alert("Role cannot be empty.");
        return;
    } else if (!userData.privacyPolicy) {
        alert("You must agree to the privacy policy!");
        return;
    }

    try {
        const response = await sendRequest(API_URL, userData);
        const newUser = await handleResponse(response);
        console.log(newUser);
        getItems();
    } catch (error) {
        console.error('Errorr:', error);
    }
}

async function sendRequest(url, data) {
    console.log("Wysyłanie żądania POST z danymi:", data);

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            firstName: data.firstName,
            lastName: data.lastName,
            role: data.role
        })
    });
    
    console.log("z serwera w sendRequest:", response);
    return response;
}

async function handleResponse(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const jsonResponse = await response.json();
    console.log("Odpowiedź JSON z serwera:", jsonResponse);
    return jsonResponse;
}

function gatherUserData() {
    return {
        firstName: document.getElementById("firstName").value.trim(),
        lastName: document.getElementById("lastName").value.trim(),
        role: document.getElementById("role").value,
        privacyPolicy: document.getElementById("privacyPolicy").checked
    };
}

function displayUsers(users) {
    const userList = document.querySelector(".users-wrapper");
    userList.innerHTML = "";

    users.forEach(user => {
        const userElement = createUserElement(user);
        userList.appendChild(userElement);
    });
}

async function getItems() {
    try {
        const response = await fetch(API_URL);
        console.log(response);

        const users = await response.json();
        console.log("Lista użytkowników pobrana z serwera:", users);
        if (Array.isArray(users)) {
            displayUsers(users);
        } else {
            console.error("Blad: Oczekiwano tablicy a otrzymano: ", users)
        }
    } catch (error) {
        console.error("Error fetching users:", error);
    }
}

document.getElementsByClassName('submit-button')[0].addEventListener('click', function(event) {
    event.preventDefault();
    sendPostRequest();
});

getItems();