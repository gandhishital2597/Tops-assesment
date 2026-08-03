// Section B - Task 2: Menu Filter & Summary
// Concepts: array of objects, filter(), map(), reduce()

const dishes = [
  { name: "Paneer Tikka",   price: 180, category: "Food",     isVegetarian: true },
  { name: "Chicken Biryani",price: 260, category: "Food",     isVegetarian: false },
  { name: "Veg Fried Rice", price: 150, category: "Food",     isVegetarian: true },
  { name: "Butter Chicken", price: 280, category: "Food",     isVegetarian: false },
  { name: "Mango Lassi",    price: 90,  category: "Beverage", isVegetarian: true },
  { name: "Cold Coffee",    price: 110, category: "Beverage", isVegetarian: true }
];

// filter(): only vegetarian dishes
const vegetarianDishes = dishes.filter(dish => dish.isVegetarian);
console.log("Vegetarian Dishes:", vegetarianDishes);

// map(): formatted display strings
const formattedMenu = dishes.map(dish => `${dish.name} - Rs ${dish.price}`);
console.log("Formatted Menu:", formattedMenu);

// reduce(): total price across the whole menu
const totalPrice = dishes.reduce((sum, dish) => sum + dish.price, 0);
console.log("Total Menu Price: Rs", totalPrice);

// Clearly labelled summary outputs
console.log("Vegetarian Dish Count:", vegetarianDishes.length);
console.log("Formatted Menu Array:", formattedMenu);
console.log("Total Price of All Dishes: Rs", totalPrice);
