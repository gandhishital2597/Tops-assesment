// Section B - Task 1: Restaurant Profile Card
// Concepts: variables (const/let), template literals, ternary operator, JSON.stringify

const restaurantName = "Spice Garden";      // never reassigned -> const
const cuisineType = "Indian";               // never reassigned -> const
let averageRating = 4.5;                    // rating could be updated as new reviews come in -> let
let isOpen = true;                          // open/closed status changes through the day -> let

// Template literal to build the formatted profile string
const profileString = `${restaurantName} | ${cuisineType} | Rating: ${averageRating} | ${isOpen ? "Open Now" : "Closed"}`;
console.log("Restaurant Profile:", profileString);

// Ternary operator used independently to display status
const statusText = isOpen ? "Open Now" : "Closed";
console.log("Current Status:", statusText);

// Serialize restaurant details into JSON
const restaurantDetails = {
  name: restaurantName,
  cuisine: cuisineType,
  rating: averageRating,
  open: isOpen
};

const restaurantJSON = JSON.stringify(restaurantDetails);
console.log("Restaurant JSON:", restaurantJSON);
