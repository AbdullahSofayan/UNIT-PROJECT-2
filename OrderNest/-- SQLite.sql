-- SQLite
-- INSERT INTO shops_shopcategory (id, name) VALUES
-- (1, 'Fast Food'),
-- (2, 'Cafe'),
-- (3, 'Bakery'),
-- (4, 'Healthy'),
-- (5, 'Seafood'),
-- (6, 'Pizza');


INSERT INTO shops_shop (id, name, contact_number, description, category_id) VALUES
(3, 'Sweet Oven', '+966551112222', 'Freshly baked goods made with love daily.', 3),
(4, 'Fit Bites','+966533334444', 'Nutritious meals and smoothies for a healthy lifestyle.', 4),
(5, 'Ocean Catch', '+966566667777', 'Serving the finest seafood straight from the Gulf.', 5),
(6, 'Slice n'' Dice','+966588889999', 'Wood-fired pizza with fresh and local toppings.', 6);

INSERT INTO shops_branch (id, shop_id, name, location) VALUES
(1, 1, 'Burger House - Exit 5', 'Exit 5, Riyadh'),
(2, 1, 'Burger House - Al Malaz', 'Al Malaz, Riyadh'),
(3, 2, 'Latte Lounge - Granada Mall', 'Granada Mall, Riyadh'),
(4, 3, 'Sweet Oven - Dhahran', 'Dhahran Mall, Al Khobar'),
(5, 5, 'Ocean Catch - Dammam Corniche', 'Corniche Rd, Dammam'),
(6, 6, 'Slice n'' Dice - Red Sea Mall', 'Red Sea Mall, Jeddah');


INSERT INTO shops_shop (id, name, contact_number, description, category_id) VALUES
(7, 'Grill Nation', '+966501234001', 'Flame-grilled chicken and beef burgers with secret sauces.', 1),
(8, 'Wrap & Roll', '+966502345002', 'Fresh wraps, fries, and fast fusion meals.', 1),
(9, 'Crispy Bites','+966503456003', 'Crispy fried chicken buckets and sides.', 1);

INSERT INTO shops_branch (id, shop_id, name, location) VALUES
(7, 7, 'Grill Nation - Riyadh Gallery', 'Riyadh Gallery Mall, Riyadh'),
(8, 8, 'Wrap & Roll - Stars Avenue', 'Stars Avenue Mall, Jeddah'),
(9, 9, 'Crispy Bites - Dhahran Mall', 'Dhahran Mall, Al Khobar');

INSERT INTO shops_shop (id, name, contact_number, description, category_id) VALUES
(10, 'Brew & Bean', '+966504567004', 'Specialty coffee and light snacks.', 2),
(11, 'Mocha Mood', '+966505678005', 'Artisanal coffee and chill atmosphere.', 2),
(12, 'The Coffee Spot', '+966506789006', 'Perfect spot for a latte by the sea.', 2);

INSERT INTO shops_branch (id, shop_id, name, location) VALUES
(10, 10, 'Brew & Bean - KAFD Tower', 'KAFD Tower A, Riyadh'),
(11, 11, 'Mocha Mood - Jeddah Waterfront', 'Jeddah Waterfront, Jeddah'),
(12, 12, 'The Coffee Spot - Dammam Seaside', 'Seaside Blvd, Dammam');

INSERT INTO accounts_user (
    username, password, email, full_name, role,
    phone, address, created_at, shop_id
)
VALUES (
    'mcdonalds',
    'pbkdf2_sha256$1000000$NNhKc3tKoXoWoc36HYo61V$oVMRNlBjKFYt766N1pg033/cmizzejchwZ3m1TdaHcE=',
    'admin1122@shop.com',
    'mcdonalds Shop',
    'admin',
    '0537348130',
    'Shop Street, Riyadh',
    '2025-07-26',
    1 
);



DELETE FROM shops_shop





-- Format: id | name           | shop_id

INSERT INTO menu_menucategory (id, name, shop_id) VALUES
(1, 'Burgers', 1),
(2, 'Drinks', 1),
(3, 'Coffee', 2),
(4, 'Pastries', 2),
(5, 'Cakes', 3),
(6, 'Hot Drinks', 3),
(7, 'Healthy Meals', 4),
(8, 'Juices', 4),
(9, 'Seafood', 5),
(10, 'Sides', 5),
(11, 'Grills', 6),
(12, 'Dips', 6),
(13, 'Steak', 7),
(14, 'Burgers', 7),
(15, 'Wraps', 8),
(16, 'Combos', 8),
(17, 'Bites', 9),
(18, 'Cold Drinks', 9),
(19, 'Espresso', 10),
(20, 'Sandwiches', 10),
(21, 'Specialty Coffee', 11),
(22, 'Desserts', 11),
(23, 'Hot Beverages', 12),
(24, 'Cookies', 12);

-- Format: id | name | description | price | calories | category_id

INSERT INTO menu_menuitem (id, name, description, price, calories, category_id) VALUES
(1, 'Classic Beef Burger', 'Grilled beef patty with cheese and lettuce', 22.00, 650, 1),
(2, 'Cheesy Chicken Burger', 'Crispy chicken with cheddar', 24.00, 720, 1),
(3, 'Coke Can', 'Chilled coke can', 6.00, 150, 2),
(4, 'Espresso', 'Strong hot espresso', 9.00, 5, 3),
(5, 'Cinnamon Roll', 'Warm and sweet cinnamon roll', 14.00, 400, 4),
(6, 'Red Velvet Cake', 'Slice of red velvet', 16.00, 450, 5),
(7, 'Green Tea', 'Healthy hot drink', 10.00, 2, 6),
(8, 'Grilled Chicken Bowl', 'Low-fat protein bowl', 27.00, 520, 7),
(9, 'Orange Juice', 'Freshly squeezed', 11.00, 120, 8),
(10, 'Shrimp Platter', 'Fried shrimp with dip', 34.00, 680, 9),
(11, 'Fries', 'Classic salted fries', 10.00, 320, 10),
(12, 'Beef Skewers', 'Marinated grilled beef', 28.00, 540, 11),
(13, 'Garlic Sauce', 'Creamy garlic dip', 3.00, 100, 12),
(14, 'Ribeye Steak', 'Juicy ribeye cooked to order', 45.00, 850, 13),
(15, 'Double Patty Burger', 'Two beef patties with cheese', 32.00, 880, 14),
(16, 'Chicken Wrap', 'Grilled chicken with veggies', 20.00, 400, 15),
(17, 'Wrap Combo', 'Wrap with fries and drink', 29.00, 750, 16),
(18, 'Mini Bites Box', 'Variety of small bites', 18.00, 520, 17),
(19, 'Lemonade', 'Refreshing lemon drink', 7.00, 130, 18),
(20, 'Americano', 'Black coffee', 10.00, 15, 19),
(21, 'Turkey Club', 'Triple layered sandwich', 21.00, 540, 20),
(22, 'Latte', 'Smooth and creamy', 13.00, 180, 21),
(23, 'Molten Cake', 'Warm chocolate cake', 16.00, 420, 22),
(24, 'Cappuccino', 'Frothy espresso', 11.00, 150, 23),
(25, 'Choco Chip Cookie', 'Soft baked cookie', 8.00, 210, 24);


INSERT INTO shops_shop (id, name, contact_number, description, category_id, rating) VALUES
(3, 'McDonald''s', '+966920006200', 'Global fast-food chain known for burgers and fries.', 1, NULL),
(4, 'Kudu', '+966920006999', 'Saudi-based fast-food restaurant known for sandwiches and meals.', 1, NULL),
(5, 'Herfy', '+966920001111', 'Popular Saudi fast-food brand offering a variety of meals.', 1, NULL),
(6, 'Dunkin'' Donuts', '+966920008899', 'American brand serving donuts, coffee, and beverages.', 2, NULL),
(7, 'Starbucks', '+966920002482', 'International coffeehouse chain offering premium coffee and snacks.', 2, NULL),
(8, 'Krispy Kreme', '+966920005488', 'Famous for its original glazed donuts and coffee drinks.', 2, NULL),
(9, 'Papa John''s', '+966920000727', 'Global pizza chain with a variety of pizza and sides.', 6, NULL),
(10, 'AlBaik', '+9668002442245', 'Famous Saudi fried chicken restaurant with unique garlic sauce.', 5, NULL),
(11, 'Subway', '+966920025288', 'International sandwich chain offering customized healthy options.', 4, NULL),
(12, 'Tim Hortons', '+966920002480', 'Canadian coffee and bakery shop known for Timbits and hot beverages.', 2, NULL);


DELETE FROM shops_branch;


UPDATE shops_shop SET id = 100 WHERE id = 3;  -- Temporary ID to avoid conflict
UPDATE shops_shop SET id = 101 WHERE id = 4;
UPDATE shops_shop SET id = 102 WHERE id = 5;
UPDATE shops_shop SET id = 103 WHERE id = 6;
UPDATE shops_shop SET id = 104 WHERE id = 7;
UPDATE shops_shop SET id = 105 WHERE id = 8;
UPDATE shops_shop SET id = 106 WHERE id = 9;
UPDATE shops_shop SET id = 107 WHERE id = 10;
UPDATE shops_shop SET id = 108 WHERE id = 11;
UPDATE shops_shop SET id = 109 WHERE id = 12;

-- Now assign the correct IDs
UPDATE shops_shop SET id = 1 WHERE id = 13;  -- McDonald's
UPDATE shops_shop SET id = 2 WHERE id = 101;  -- Kudu
UPDATE shops_shop SET id = 3 WHERE id = 14;  -- Herfy
UPDATE shops_shop SET id = 4 WHERE id = 103;  -- Dunkin'
UPDATE shops_shop SET id = 5 WHERE id = 104;  -- Starbucks
UPDATE shops_shop SET id = 6 WHERE id = 105;  -- Krispy Kreme
UPDATE shops_shop SET id = 7 WHERE id = 106;  -- Papa John's
UPDATE shops_shop SET id = 8 WHERE id = 107;  -- AlBaik
UPDATE shops_shop SET id = 9 WHERE id = 108;  -- Subway
UPDATE shops_shop SET id = 10 WHERE id = 109; -- Tim Hortons

UPDATE menu_menucategory SET shop_id = 1 where id = 25; 
UPDATE menu_menucategory SET shop_id = 1 where id = 26; 

UPDATE shops_shop SET name = "McDonald's" WHERE id = 1;


ALTER TABLE shops_shop DROP COLUMN image;


DELETE FROM accounts_user WHERE id = 2;


UPDATE accounts_user set password = "pbkdf2_sha256$1000000$NNhKc3tKoXoWoc36HYo61V$oVMRNlBjKFYt766N1pg033/cmizzejchwZ3m1TdaHcE=" where id = 5;

INSERT INTO accounts_user ()


INSERT INTO menu_menuitem (name, description, price, calories, category_id)
VALUES 
('McCrispy Chicken', 'Chicken sandwich', 25, 450, 29),
('McCrispy Chicken Deluxe', 'Deluxe chicken sandwich', 27, 480, 29),
('Big Tasty', 'Big beef burger', 28, 510, 29),
('Big Tasty Chicken', 'Chicken version of Big Tasty', 26, 500, 29),
('Grand Chicken Special', 'Special chicken sandwich', 27, 530, 29),
('Big Tasty Mushroom', 'Mushroom beef burger', 29, 550, 29),
('Grand Chicken Spicy', 'Spicy chicken sandwich', 26, 460, 29),
('Grand Chicken Deluxe', 'Deluxe Grand Chicken', 28, 490, 29),
('Big Mac', 'Double beef patties with lettuce, cheese, pickles, and special sauce', 25, 258, 29),
('Chicken Mac', 'Double chicken patties', 24, 420, 29),
('Spicy McChicken', 'Spicy version of McChicken', 22, 400, 29),
('McChicken', 'Classic chicken burger', 20, 380, 29),
('Quarter Pounder', 'Beef patty with cheese', 23, 430, 29),
('Chicken McArabia', 'Grilled chicken with Arabic bread', 27, 410, 29),
('Chicken McNuggets', 'Chicken nuggets 6 pcs', 18, 300, 29),
('Triple Cheeseburger', 'Triple layers of cheese and beef', 30, 600, 29),
('Little Tasty Chicken', 'Mini Big Tasty Chicken', 19, 350, 29),
('McWings Peri Peri', 'Spicy chicken wings', 22, 320, 29),
('McWings Chicken Regular', 'Regular wings', 20, 300, 29),
('Double Cheeseburger', 'Double beef and cheese', 28, 580, 29),
('Chicken Burger', 'Simple chicken sandwich', 15, 260, 29),
('Cheeseburger', 'Classic cheeseburger', 18, 300, 29),
('Beef Burger', 'Grilled beef patty', 21, 310, 29),
('Mini Kofta', 'Small kofta wrap', 20, 280, 29),
('Mini Arabia', 'Mini Arabic sandwich', 17, 250, 29),
('McArabia Kofta', 'Kofta with Arabic bread', 27, 350, 29),
('McRoyale', 'Premium beef burger', 32, 650, 29);

UPDATE menu_menuitem SET category_id = 25 WHERE category_id = 29;

DELETE from orders_orderitemoption;



INSERT INTO accounts_user (username, password, email, full_name, role, phone, created_at, shop_id) VALUES
('mcdonalds', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@mcdonalds.com', 'McDonalds Admin', 'admin', '920000001', '2025-07-28', 1),
('kudu', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@kudu.com', 'Kudu Admin', 'admin', '966920006999', '2025-07-28', 2),
('herfy', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@herfy.com', 'Herfy Admin', 'admin', '920000002', '2025-07-28', 3),
('dunkindonuts', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@dunkin.com', 'Dunkin Donuts Admin', 'admin', '966920008899', '2025-07-28', 4),
('starbucks', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@starbucks.com', 'Starbucks Admin', 'admin', '966920002482', '2025-07-28', 5),
('krispykreme', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@krispykreme.com', 'Krispy Kreme Admin', 'admin', '966920005488', '2025-07-28', 6),
('papajohns', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@papajohns.com', 'Papa Johns Admin', 'admin', '966920000727', '2025-07-28', 7),
('albaik', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@albaik.com', 'AlBaik Admin', 'admin', '9668002442245', '2025-07-28', 8),
('subway', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@subway.com', 'Subway Admin', 'admin', '966920025288', '2025-07-28', 9),
('timhortons', 'pbkdf2_sha256$100000$suriz2gcl2rz6qJfJrts4zQ8Vu4ArkqsIq2xt/4uQ1GNz8DQ+2wD5q5oaZ0QBunC//g=', 'admin@timhortons.com', 'Tim Hortons Admin', 'admin', '966920002480', '2025-07-28', 10);







INSERT INTO menu_menuitem (name, description, price, calories, category_id, shop_id)
VALUES 
('Double Cheesy Bacon Fries', 'Double the indulgence with crispy fries, cheddar cheese, burrito sauce, crispy bacon, and jalapeños.', 20, 520, 42, 2),
('Cheesy Bacon Fries', 'Indulge in crispy French fries loaded with cheddar cheese, burrito sauce, crispy bacon, and green onions.', 16, 450, 42, 2),
('French Cheese Bites', 'The delicious 4pcs French cheese bites is here in a new form with French cheese and dipping sauce.', 16, 390, 42, 2);


