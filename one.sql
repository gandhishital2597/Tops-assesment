Database Management – SQL & PL/SQL
Theme: Personal Expense Tracker DB
Section A: Concept Application

1.Explain how relational databases help maintain accuracy in expense records.
Ans : -  Relational databases maintain accuracy in expense records by storing data in structured tables and linking them using primary and foreign keys. This ensures that each record is unique and correctly related (for example, every expense must belong to a valid user or category).
They enforce data integrity through constraints like NOT NULL, UNIQUE, and referential integrity, which prevent invalid or duplicate data. Additionally, ACID properties of transactions ensure that all operations are completed fully and consistently, even in case of failures.
Overall, this reduces redundancy, avoids errors, and keeps expense data accurate and reliable—making it ideal for systems like a Personal Expense Tracker.

2.Why are constraints important in personal finance data ?
Ans :- Constraints act as rules that protect financial data from mistakes, ensuring reliable tracking and decision-making.
  - Constraints are important in personal finance data because they ensure the data is accurate, valid, and consistent.

They prevent common errors such as:

Invalid entries (e.g., expense amount cannot be NULL or negative)
Duplicate records (using UNIQUE or primary keys)
Wrong relationships (foreign keys ensure each expense belongs to a valid user or category)

This helps maintain data integrity, which is critical in finance because even small errors can lead to incorrect balances or reports.
 
3.. How does GROUP BY help analyze spending patterns?
Ans :- GROUP BY converts raw expense data into meaningful summaries for analysis. 
 -GROUP BY helps analyze spending patterns by organizing expense data into categories or groups and then applying aggregate functions (like SUM, COUNT, AVG).

For example:

Grouping by category shows how much is spent on food, travel, etc.
Grouping by month helps track monthly spending trends.
Using SUM(amount) with GROUP BY gives total expenses per group.

This makes it easier to identify patterns, compare spending, and make better financial decisions. 

4. Explain loop usage for monthly summaries.
Ans : - Loops automate repetitive calculations, making it easy to generate monthly expense summaries efficiently. 
  - Loops are used in PL/SQL to process and summarize data repeatedly, such as calculating monthly expenses.

For monthly summaries:

A loop can iterate through each month (1 to 12) or through records of expenses.
Inside the loop, it calculates totals using queries like SUM(amount) for that specific month.
The result for each month is stored or displayed.

Example idea:-
Loop through months → fetch total expenses for each month → print/store summary.

5. Explain why collections suit transaction storage.
Ans :- Collections provide a fast, flexible, and efficient way to manage multiple transaction records during processing.  
  - Collections in PL/SQL are suitable for transaction storage because they allow handling multiple records in memory as a group, which is ideal for frequent and dynamic financial transactions.

They store data like arrays or lists (e.g., multiple expenses) for quick access and processing.
Reduce database calls by processing data in bulk → improves performance.
Flexible structure (Nested Tables, VARRAYs, Associative Arrays) allows dynamic addition/removal of transactions.
Useful for temporary calculations like totals, filtering, or batch updates.

6. Explain payment modes using polymorphism.  ?
Ans -  Polymorphism lets you treat all payment modes uniformly while executing their specific payment logic, making the system flexible and easy to extend. 
  - Polymorphism means one interface, multiple implementations. In payment modes, it allows different payment types to be handled using a common method.
Example: Create a base type/class Payment with a method pay().
Different modes like CashPayment, CardPayment, UPIPayment override the same pay() method with their own logic.
So when calling pay(), the system automatically executes the correct behavior based on the actual payment type.
-- ============================================================================
-- TOPS TECHNOLOGIES - DATABASE MANAGEMENT: SQL & PL/SQL
-- Theme: Personal Expense Tracker DB
-- SOFTWARE ENGINEERING [Database Management - SQL & PL/SQL - A1]
-- ============================================================================


-- ============================================================================
-- DATABASE SETUP
-- ============================================================================

CREATE DATABASE IF NOT EXISTS expense_tracker;
USE expense_tracker;


-- ============================================================================
-- GIVEN SCHEMA (DO NOT MODIFY)
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    user_id    INT PRIMARY KEY,
    name       VARCHAR(50),
    email      VARCHAR(100),
    created_at DATE
);

CREATE TABLE IF NOT EXISTS categories (
    category_id   INT PRIMARY KEY,
    category_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS expenses (
    expense_id   INT PRIMARY KEY,
    user_id      INT,
    category_id  INT,
    amount       DECIMAL(10,2),
    expense_date DATE,
    FOREIGN KEY (user_id)     REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);


-- ============================================================================
-- SECTION B: SQL HANDS-ON
-- ============================================================================

-- ----------------------------------------------------------------------------
-- B2. DML OPERATIONS
-- ----------------------------------------------------------------------------

-- ----------------------------------------
-- INSERT 5 Users
-- ----------------------------------------
INSERT INTO users (user_id, name, email, created_at) VALUES
(1, 'Aarav Shah',    'aarav.shah@gmail.com',    '2024-01-10'),
(2, 'Priya Mehta',   'priya.mehta@gmail.com',   '2024-02-15'),
(3, 'Ravi Patel',    'ravi.patel@gmail.com',    '2024-03-05'),
(4, 'Sneha Joshi',   'sneha.joshi@gmail.com',   '2024-04-20'),
(5, 'Karan Desai',   'karan.desai@gmail.com',   '2024-05-01');

-- ----------------------------------------
-- INSERT 3 Categories
-- ----------------------------------------
INSERT INTO categories (category_id, category_name) VALUES
(1, 'Food'),
(2, 'Rent'),
(3, 'Entertainment');

-- ----------------------------------------
-- INSERT 10 Expense Records
-- ----------------------------------------
INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date) VALUES
(101, 1, 1, 850.00,  '2025-01-05'),   -- Aarav, Food
(102, 1, 2, 8000.00, '2025-01-10'),   -- Aarav, Rent
(103, 2, 1, 1200.00, '2025-01-12'),   -- Priya, Food
(104, 2, 3, 500.00,  '2025-01-18'),   -- Priya, Entertainment
(105, 3, 1, 650.00,  '2025-01-20'),   -- Ravi, Food
(106, 3, 2, 7500.00, '2025-01-22'),   -- Ravi, Rent
(107, 4, 3, 1500.00, '2025-01-25'),   -- Sneha, Entertainment
(108, 4, 1, 900.00,  '2025-01-28'),   -- Sneha, Food
(109, 5, 2, 9000.00, '2025-01-30'),   -- Karan, Rent
(110, 5, 3, 300.00,  '2025-02-01');   -- Karan, Entertainment

-- ----------------------------------------
-- UPDATE: Fix incorrect expense amount
-- (expense_id 105: was 650.00, correct is 750.00)
-- ----------------------------------------
UPDATE expenses
SET    amount = 750.00
WHERE  expense_id = 105;

-- ----------------------------------------
-- DELETE: Remove expense where amount < 400
-- (expense_id 110 has amount 300.00)
-- ----------------------------------------
DELETE FROM expenses
WHERE amount < 400.00;


-- ----------------------------------------------------------------------------
-- B3. DATA RETRIEVAL
-- ----------------------------------------------------------------------------

-- ----------------------------------------
-- Query 1: Display all expenses with details
-- (expense_date, amount, user name, category_name using INNER JOIN)
-- ----------------------------------------
SELECT
    e.expense_id,
    e.expense_date,
    e.amount,
    u.name          AS user_name,
    c.category_name
FROM expenses   e
INNER JOIN users      u ON e.user_id     = u.user_id
INNER JOIN categories c ON e.category_id = c.category_id
ORDER BY e.expense_date;

-- ----------------------------------------
-- Query 2: Total expense amount per category
-- (SUM + GROUP BY category_name)
-- ----------------------------------------
SELECT
    c.category_name,
    SUM(e.amount)  AS total_spent
FROM expenses   e
INNER JOIN categories c ON e.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_spent DESC;

-- ----------------------------------------
-- Query 3: Users sorted by total spending (highest to lowest)
-- ----------------------------------------
SELECT
    u.name,
    SUM(e.amount)  AS total_spending
FROM expenses   e
INNER JOIN users u ON e.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY total_spending DESC;


-- ----------------------------------------------------------------------------
-- B4. VIEWS
-- ----------------------------------------------------------------------------

-- ----------------------------------------
-- Create ActiveUsersView:
-- Users who have logged MORE than 5 expense records
-- ----------------------------------------
CREATE OR REPLACE VIEW ActiveUsersView AS
SELECT
    u.name,
    u.email,
    COUNT(e.expense_id) AS total_expenses
FROM users    u
INNER JOIN expenses e ON u.user_id = e.user_id
GROUP BY u.user_id, u.name, u.email
HAVING COUNT(e.expense_id) > 5;

-- ----------------------------------------
-- Query the view
-- ----------------------------------------
SELECT * FROM ActiveUsersView;


-- ============================================================================
-- SECTION C: MINI PROJECT - EXPENSE TRACKER DB
-- ============================================================================


-- ----------------------------------------------------------------------------
-- C1. CRUD QUERIES (Create, Read, Update, Delete)
-- ----------------------------------------------------------------------------

-- CREATE: Add a new user
INSERT INTO users (user_id, name, email, created_at)
VALUES (6, 'Meera Nair', 'meera.nair@gmail.com', CURDATE());

-- CREATE: Add a new expense for the new user
INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
VALUES (111, 6, 1, 1100.00, CURDATE());

-- READ: View all expenses for a specific user (user_id = 1)
SELECT
    e.expense_id,
    e.expense_date,
    c.category_name,
    e.amount
FROM expenses   e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = 1
ORDER BY e.expense_date DESC;

-- READ: View all users and their expense count
SELECT
    u.name,
    COUNT(e.expense_id) AS num_expenses,
    COALESCE(SUM(e.amount), 0) AS total_spent
FROM users    u
LEFT JOIN expenses e ON u.user_id = e.user_id
GROUP BY u.user_id, u.name;

-- UPDATE: Correct the amount for a specific expense
UPDATE expenses
SET    amount = 950.00
WHERE  expense_id = 101;

-- UPDATE: Change a user's email
UPDATE users
SET    email = 'aarav.updated@gmail.com'
WHERE  user_id = 1;

-- DELETE: Remove an expense by expense_id
DELETE FROM expenses
WHERE expense_id = 111;

-- DELETE: Remove all expenses older than a specific date (for cleanup)
-- DELETE FROM expenses WHERE expense_date < '2024-01-01';
-- (Commented out to protect sample data)


-- ----------------------------------------------------------------------------
-- C2. STORED PROCEDURE: Calculate Monthly User Expense
-- ----------------------------------------------------------------------------

DELIMITER $$

CREATE PROCEDURE GetMonthlyExpense(
    IN  p_user_id INT,
    IN  p_month   INT,
    IN  p_year    INT,
    OUT p_total   DECIMAL(10,2)
)
BEGIN
    -- Calculate total expenses for a given user, month, and year
    SELECT COALESCE(SUM(amount), 0)
    INTO   p_total
    FROM   expenses
    WHERE  user_id             = p_user_id
      AND  MONTH(expense_date) = p_month
      AND  YEAR(expense_date)  = p_year;

    -- Display a summary report
    SELECT
        u.name                          AS user_name,
        p_month                         AS month,
        p_year                          AS year,
        c.category_name,
        SUM(e.amount)                   AS category_total
    FROM expenses   e
    JOIN users      u ON e.user_id     = u.user_id
    JOIN categories c ON e.category_id = c.category_id
    WHERE e.user_id             = p_user_id
      AND MONTH(e.expense_date) = p_month
      AND YEAR(e.expense_date)  = p_year
    GROUP BY c.category_name
    ORDER BY category_total DESC;
END$$

DELIMITER ;

-- ----------------------------------------
-- How to CALL the stored procedure:
-- ----------------------------------------
-- Declare an output variable and call the procedure:

SET @total_expense = 0;
CALL GetMonthlyExpense(1, 1, 2025, @total_expense);
SELECT @total_expense AS total_monthly_expense;

-- This will:
-- 1. Show a category-wise breakdown for user_id=1 in January 2025
-- 2. Store the total amount in @total_expense variable


-- ----------------------------------------------------------------------------
-- C3. COMMIT and ROLLBACK DEMONSTRATION
-- ----------------------------------------------------------------------------

-- ----------------------------------------
-- Example 1: Successful Transaction (COMMIT)
-- Insert two valid expenses atomically
-- ----------------------------------------
START TRANSACTION;

    INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
    VALUES (201, 2, 1, 600.00, '2025-02-10');

    INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
    VALUES (202, 2, 3, 1200.00, '2025-02-11');

    -- Both inserts are valid -- save permanently
COMMIT;
-- All changes are now permanently saved in the database.

-- ----------------------------------------
-- Example 2: Failed Transaction (ROLLBACK)
-- Simulate a failure: second insert has invalid user_id
-- ----------------------------------------
START TRANSACTION;

    INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
    VALUES (203, 3, 2, 7000.00, '2025-02-12');

    -- This will FAIL: user_id 999 does not exist (FK violation)
    -- INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
    -- VALUES (204, 999, 1, 500.00, '2025-02-12');

    -- Since the second operation would fail, we ROLLBACK everything:
ROLLBACK;
-- expense_id 203 is also undone. DB is clean.

-- ----------------------------------------
-- Example 3: SAVEPOINT -- Partial Rollback
-- Roll back only part of a transaction
-- ----------------------------------------
START TRANSACTION;

    INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
    VALUES (205, 4, 1, 800.00, '2025-02-15');

    SAVEPOINT after_first_insert;  -- mark a save point here

    INSERT INTO expenses (expense_id, user_id, category_id, amount, expense_date)
    VALUES (206, 4, 3, 2000.00, '2025-02-15');

    -- Suppose we realize expense 206 was entered by mistake:
    ROLLBACK TO after_first_insert;  -- only expense 206 is undone

    -- expense 205 is still in the transaction
COMMIT;
-- Only expense 205 is permanently saved.


-- ============================================================================
-- ADDITIONAL USEFUL QUERIES FOR EXPENSE TRACKER
-- ============================================================================

-- 1. Top spending category overall
SELECT
    c.category_name,
    SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total DESC
LIMIT 1;

-- 2. Monthly spending trend for all users
SELECT
    YEAR(expense_date)  AS yr,
    MONTH(expense_date) AS mo,
    SUM(amount)         AS monthly_total
FROM expenses
GROUP BY YEAR(expense_date), MONTH(expense_date)
ORDER BY yr, mo;

-- 3. Users who have NOT entered any expense (LEFT JOIN)
SELECT u.name, u.email
FROM users u
LEFT JOIN expenses e ON u.user_id = e.user_id
WHERE e.expense_id IS NULL;

-- 4. Average expense per user
SELECT
    u.name,
    ROUND(AVG(e.amount), 2) AS avg_expense
FROM expenses e
JOIN users u ON e.user_id = u.user_id
GROUP BY u.user_id, u.name
ORDER BY avg_expense DESC;

-- 5. Highest single expense record
SELECT
    e.expense_id,
    u.name,
    c.category_name,
    e.amount,
    e.expense_date
FROM expenses e
JOIN users      u ON e.user_id     = u.user_id
JOIN categories c ON e.category_id = c.category_id
ORDER BY e.amount DESC
LIMIT 1;

-- 6. Create a trigger: Auto-log expense inserts to audit table
-- (First create audit table)
CREATE TABLE IF NOT EXISTS expense_audit (
    audit_id    INT AUTO_INCREMENT PRIMARY KEY,
    expense_id  INT,
    user_id     INT,
    amount      DECIMAL(10,2),
    action_type VARCHAR(10),
    action_time DATETIME
);

DELIMITER $$
CREATE TRIGGER trg_after_expense_insert
AFTER INSERT ON expenses
FOR EACH ROW
BEGIN
    INSERT INTO expense_audit (expense_id, user_id, amount, action_type, action_time)
    VALUES (NEW.expense_id, NEW.user_id, NEW.amount, 'INSERT', NOW());
END$$
DELIMITER ;


-- ============================================================================
-- END OF SQL FILE - PERSONAL EXPENSE TRACKER DB
-- Prepared for: TOPS Technologies | SOFTWARE ENGINEERING [SQL & PL/SQL - A1]
-- ============================================================================
