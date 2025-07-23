-- SQLite
-- INSERT INTO shops_shopcategory (id, name) VALUES
-- (1, 'Fast Food'),
-- (2, 'Cafe'),
-- (3, 'Bakery'),
-- (4, 'Healthy'),
-- (5, 'Seafood'),
-- (6, 'Pizza');


-- INSERT INTO shops_shop (id, name, location, contact_number, description, category_id) VALUES
-- (1, 'Burger House', 'King Fahd Rd, Riyadh', '+966501234567', 'Home of delicious grilled burgers with a Saudi twist.', 1),
-- (2, 'Latte Lounge', 'Olaya St, Riyadh', '+966509876543', 'Cozy cafe serving premium coffee and desserts.', 2),
-- (3, 'Sweet Oven', 'Al Khobar Corniche', '+966551112222', 'Freshly baked goods made with love daily.', 3),
-- (4, 'Fit Bites', 'King Abdulaziz Rd, Jeddah', '+966533334444', 'Nutritious meals and smoothies for a healthy lifestyle.', 4),
-- (5, 'Ocean Catch', 'Corniche Rd, Dammam', '+966566667777', 'Serving the finest seafood straight from the Gulf.', 5),
-- (6, 'Slice n'' Dice', 'Prince Sultan Rd, Jeddah', '+966588889999', 'Wood-fired pizza with fresh and local toppings.', 6);

INSERT INTO shops_branch (id, shop_id, name, location) VALUES
(1, 1, 'Burger House - Exit 5', 'Exit 5, Riyadh'),
(2, 1, 'Burger House - Al Malaz', 'Al Malaz, Riyadh'),
(3, 2, 'Latte Lounge - Granada Mall', 'Granada Mall, Riyadh'),
(4, 3, 'Sweet Oven - Dhahran', 'Dhahran Mall, Al Khobar'),
(5, 5, 'Ocean Catch - Dammam Corniche', 'Corniche Rd, Dammam'),
(6, 6, 'Slice n'' Dice - Red Sea Mall', 'Red Sea Mall, Jeddah');


INSERT INTO shops_shop (id, name, location, contact_number, description, category_id) VALUES
(7, 'Grill Nation', 'Al Yasmin, Riyadh', '+966501234001', 'Flame-grilled chicken and beef burgers with secret sauces.', 1),
(8, 'Wrap & Roll', 'Tahlia St, Jeddah', '+966502345002', 'Fresh wraps, fries, and fast fusion meals.', 1),
(9, 'Crispy Bites', 'Al Khobar Plaza, Al Khobar', '+966503456003', 'Crispy fried chicken buckets and sides.', 1);

INSERT INTO shops_branch (id, shop_id, name, location) VALUES
(7, 7, 'Grill Nation - Riyadh Gallery', 'Riyadh Gallery Mall, Riyadh'),
(8, 8, 'Wrap & Roll - Stars Avenue', 'Stars Avenue Mall, Jeddah'),
(9, 9, 'Crispy Bites - Dhahran Mall', 'Dhahran Mall, Al Khobar');

INSERT INTO shops_shop (id, name, location, contact_number, description, category_id) VALUES
(10, 'Brew & Bean', 'King Abdullah Financial District, Riyadh', '+966504567004', 'Specialty coffee and light snacks.', 2),
(11, 'Mocha Mood', 'Red Sea Mall, Jeddah', '+966505678005', 'Artisanal coffee and chill atmosphere.', 2),
(12, 'The Coffee Spot', 'Corniche Walk, Dammam', '+966506789006', 'Perfect spot for a latte by the sea.', 2);

INSERT INTO shops_branch (id, shop_id, name, location) VALUES
(10, 10, 'Brew & Bean - KAFD Tower', 'KAFD Tower A, Riyadh'),
(11, 11, 'Mocha Mood - Jeddah Waterfront', 'Jeddah Waterfront, Jeddah'),
(12, 12, 'The Coffee Spot - Dammam Seaside', 'Seaside Blvd, Dammam');

INSERT INTO accounts_user (
    username, password, email, full_name, role,
    phone, address, created_at, shop_id
)
VALUES (
    'admin1122',
    'admin',
    'admin@shop.com',
    'Admin Shop',
    'admin',
    '0555555555',
    'Shop Street, Riyadh',
    '2025-07-23',
    1 
);






