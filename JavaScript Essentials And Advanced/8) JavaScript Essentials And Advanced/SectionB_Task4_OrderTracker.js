// Section B - Task 4: Order Tracker with Persistence

const restaurantListEl = document.getElementById("restaurantList");
const statusEl = document.getElementById("status");
const errorMsgEl = document.getElementById("errorMsg");

const FAVOURITE_KEY = "favouriteRestaurant";

async function loadRestaurants() {
  try {
    const response = await fetch("https://jsonplaceholder.typicode.com/users");

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const users = await response.json();
    statusEl.textContent = "";
    renderRestaurants(users);
  } catch (err) {
    statusEl.textContent = "";
    errorMsgEl.textContent = "Could not load restaurant list. Please try again later.";
    console.error(err);
  }
}

function renderRestaurants(users) {
  const savedFavourite = localStorage.getItem(FAVOURITE_KEY);

  users.forEach(user => {
    const li = document.createElement("li");
    li.textContent = user.name; // treating each user record as a mock restaurant entry
    li.dataset.name = user.name;

    if (savedFavourite === user.name) {
      li.classList.add("favourite");
    }

    li.addEventListener("click", () => {
      // Remove highlight from any previously selected item
      document.querySelectorAll("#restaurantList li").forEach(item => {
        item.classList.remove("favourite");
      });

      li.classList.add("favourite");
      localStorage.setItem(FAVOURITE_KEY, user.name);
    });

    restaurantListEl.appendChild(li);
  });
}

loadRestaurants();
