// Section B - Task 3: Live Order Form (DOM + Events)

const dishNameInput = document.getElementById("dishName");
const quantityInput = document.getElementById("quantity");
const dishError = document.getElementById("dishError");
const qtyError = document.getElementById("qtyError");
const addToCartBtn = document.getElementById("addToCartBtn");
const cartList = document.getElementById("cartList");

addToCartBtn.addEventListener("click", function (event) {
  event.preventDefault(); // prevents any default browser behaviour (e.g. if button were type="submit")

  // Reset previous error messages
  dishError.textContent = "";
  qtyError.textContent = "";

  const dishName = dishNameInput.value.trim();
  const quantity = quantityInput.value.trim();

  let isValid = true;

  if (dishName === "") {
    dishError.textContent = "Dish name cannot be empty.";
    isValid = false;
  }

  if (quantity === "") {
    qtyError.textContent = "Quantity cannot be empty.";
    isValid = false;
  }

  if (!isValid) return;

  // Append new cart item
  const li = document.createElement("li");
  li.textContent = `${dishName} x ${quantity}`;
  cartList.appendChild(li);

  // Clear inputs for next entry
  dishNameInput.value = "";
  quantityInput.value = "";
});
