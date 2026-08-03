# M1 — JavaScript Essentials and Advanced (ReactJS Track, M1-A1)

This repo contains the full submission for the **M1-A1 JavaScript Essentials and Advanced**
assessment: written concept answers, standalone practical coding tasks, a combined mini
capstone app, and an AI-augmented learning exercise.

## Repository contents

| File | Section | Type |
|---|---|---|
| `SectionA_ConceptApplication.md` / `.docx` | A — Concept Application | Written answers |
| `SectionB_Task1_RestaurantProfileCard.js` | B — Task 1 | Console script |
| `SectionB_Task2_MenuFilterSummary.js` | B — Task 2 | Console script |
| `SectionB_Task3_LiveOrderForm.html` + `.js` | B — Task 3 | Browser app |
| `SectionB_Task4_OrderTracker.html` + `.js` | B — Task 4 | Browser app |
| `SectionC_MiniCapstone_FoodDeliveryApp.html` | C — Mini Capstone | Browser app |
| `SectionD_Prompt_and_Notes.md` / `.docx` | D — AI-Augmented Learning | Notes |
| `SectionD_AI_Original.html` | D — AI-Augmented Learning | Buggy AI-generated code |
| `SectionD_AI_Corrected.html` | D — AI-Augmented Learning | Fixed, working code |

No build tools, bundlers, or frameworks are used — everything runs directly in a browser or
with plain Node.js.

---

## Section A — Concept Application

Six scenario-based questions on `var`/`let`/`const`, conditionals, loops, function types,
DOM events, and promises vs. `async`/`await`.

**How to view:** open `SectionA_ConceptApplication.md` in any markdown viewer (GitHub renders
it automatically), or open `SectionA_ConceptApplication.docx` in Microsoft Word / Google Docs.
No setup required — this section is read-only reference material, not runnable code.

---

## Section B — Practical Coding Tasks

### Task 1: Restaurant Profile Card (console-based)
**Run:**
```bash
node SectionB_Task1_RestaurantProfileCard.js
```
Logs a formatted restaurant profile string, an open/closed status via ternary, and a
`JSON.stringify()` output — all in the terminal.

### Task 2: Menu Filter & Summary (console-based)
**Run:**
```bash
node SectionB_Task2_MenuFilterSummary.js
```
Logs the filtered vegetarian dishes, a `map()`-formatted menu list, and a `reduce()`-based
total price.

### Task 3: Live Order Form (browser-based)
**Files:** `SectionB_Task3_LiveOrderForm.html`, `SectionB_Task3_LiveOrderForm.js`
**Run:** double-click `SectionB_Task3_LiveOrderForm.html` to open it in any browser (or right
click → Open With → your browser). No server needed.
**Try it:** enter a dish name and quantity, click **Add to Cart** — it validates both fields
and appends the item to the on-page cart list without reloading the page.

### Task 4: Order Tracker with Persistence (browser-based)
**Files:** `SectionB_Task4_OrderTracker.html`, `SectionB_Task4_OrderTracker.js`
**Run:** open `SectionB_Task4_OrderTracker.html` in a browser.
**Requires internet access** (fetches `https://jsonplaceholder.typicode.com/users`).
**Try it:** click any restaurant name to save it as your favourite (highlighted + saved to
`localStorage`); refresh the page and your favourite stays highlighted automatically.

---

## Section C — Mini Capstone: Interactive Food Delivery Menu App

**File:** `SectionC_MiniCapstone_FoodDeliveryApp.html` (single self-contained file — HTML, CSS,
and JS all in one place, no separate assets needed)

**Run:** open the file directly in a browser. **Requires internet access** for the restaurant
selector dropdown (same public API as Task 4).

**What it does:**
- **Browse Menu** tab — 7 dynamically rendered dish cards (name, price, category, veg/non-veg
  tag) each with an **Add to Cart** button.
- **View Cart** tab — live item list with quantity +/- controls and a running total; the tab
  label shows a live cart-count badge.
- **Clear Cart** tab — wipes the cart with one click.
- The cart is saved to `localStorage` on every change and automatically reloaded on page
  refresh, so it survives a browser reload.

> **Why C isn't just a copy of B:** the capstone brief asks you to combine DOM manipulation,
> events, array methods, `fetch`/`async`-`await`, and `localStorage` into *one* working app, so
> this file is the "real" integrated deliverable — Task 3/4 remain as their own separate files
> since the assessment explicitly asks for each B task individually too.

---

## Section D — AI-Augmented Learning

Demonstrates the required workflow: **build with AI → test without AI → find and fix a bug.**

1. Read `SectionD_Prompt_and_Notes.md` (or `.docx`) first — it has the exact prompt given to the
   AI tool and a written explanation of the bug that was found and fixed.
2. Open `SectionD_AI_Original.html` in a browser. **Requires internet access**
   (fetches `https://jsonplaceholder.typicode.com/posts`).
   - **Reproduce the bug:** click **Add to Favourites** next to *any* item in the list — notice
     it always favourites the *last* item in the list instead of the one you clicked. This is a
     classic `var` closure-in-a-loop bug.
3. Open `SectionD_AI_Corrected.html` in a browser and repeat the same click — each button now
   correctly favourites (and can un-favourite) its own item, and multiple favourites persist
   correctly across a page refresh.

---

## General setup

No installation is required to **view or run** any of the HTML/JS files — modern browsers
run vanilla JavaScript natively.

If you want to run the console tasks (`Task 1`, `Task 2`) and don't have Node.js installed:

1. Install [Node.js](https://nodejs.org/) (LTS version is fine).
2. Verify the install:
   ```bash
   node -v
   ```
3. Run any script with:
   ```bash
   node <filename>.js
   ```

For the browser-based files (Tasks 3 & 4, Section C, Section D), simply open the `.html` file
in Chrome, Firefox, or Edge — no server, bundler, or extra dependencies needed. An internet
connection is required only for the files that call the public
`jsonplaceholder.typicode.com` API (Task 4, Section C, Section D).

## Taking screenshots for submission

Per the assessment's general instructions:
- **Console tasks (1, 2):** run with `node`, then screenshot the terminal output.
- **Browser tasks (3, 4, C, D):** open the `.html` file, interact with it as described above,
  then screenshot the browser window showing the working result.
