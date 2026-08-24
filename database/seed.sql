-- Calorify Sample Seed Data for Local Development
USE calorify;

-- Seed Demo User
INSERT INTO users (firebase_uid, name, email, calorie_goal)
VALUES ('demo_user_12345', 'Demo User', 'demo@calorify.app', 2200)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Seed Sample Meals
INSERT INTO food_entries (firebase_uid, food_name, meal, calories, protein, carbs, fat, fiber, consumed_at)
VALUES 
('demo_user_12345', 'Avocado Toast with Poached Egg', 'Breakfast', 380, 14.5, 32.0, 22.0, 6.5, NOW() - INTERVAL 8 HOUR),
('demo_user_12345', 'Greek Yogurt with Blueberries', 'Breakfast', 180, 15.0, 20.0, 3.5, 2.0, NOW() - INTERVAL 7 HOUR),
('demo_user_12345', 'Grilled Chicken Quinoa Bowl', 'Lunch', 550, 42.0, 52.0, 16.0, 7.0, NOW() - INTERVAL 4 HOUR),
('demo_user_12345', 'Roasted Almonds & Green Apple', 'Snack', 210, 5.0, 24.0, 12.0, 4.0, NOW() - INTERVAL 2 HOUR)
ON DUPLICATE KEY UPDATE food_name=VALUES(food_name);

-- Seed Daily Activity Log
INSERT INTO daily_logs (firebase_uid, log_date, water_ml, exercise_minutes)
VALUES ('demo_user_12345', CURRENT_DATE(), 1750, 45)
ON DUPLICATE KEY UPDATE water_ml=VALUES(water_ml), exercise_minutes=VALUES(exercise_minutes);
