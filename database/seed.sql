-- Optional PostgreSQL seed data for local development.
-- Run this after the tables exist.

INSERT INTO users (firebase_uid, name, email, calorie_goal)
VALUES ('demo_user_12345', 'Demo User', 'demo@calorify.app', 2200)
ON CONFLICT (firebase_uid) DO UPDATE SET name = EXCLUDED.name, calorie_goal = EXCLUDED.calorie_goal;

INSERT INTO food_entries (firebase_uid, food_name, meal, calories, protein, carbs, fat, fiber, consumed_at)
VALUES
('demo_user_12345', 'Avocado Toast with Poached Egg', 'Breakfast', 380, 14.5, 32.0, 22.0, 6.5, CURRENT_TIMESTAMP - INTERVAL '8 hours'),
('demo_user_12345', 'Greek Yogurt with Blueberries', 'Breakfast', 180, 15.0, 20.0, 3.5, 2.0, CURRENT_TIMESTAMP - INTERVAL '7 hours'),
('demo_user_12345', 'Grilled Chicken Quinoa Bowl', 'Lunch', 550, 42.0, 52.0, 16.0, 7.0, CURRENT_TIMESTAMP - INTERVAL '4 hours'),
('demo_user_12345', 'Roasted Almonds & Green Apple', 'Snack', 210, 5.0, 24.0, 12.0, 4.0, CURRENT_TIMESTAMP - INTERVAL '2 hours');

INSERT INTO daily_logs (firebase_uid, log_date, water_ml, exercise_minutes)
VALUES ('demo_user_12345', CURRENT_DATE, 1750, 0)
ON CONFLICT (firebase_uid, log_date) DO UPDATE SET water_ml = EXCLUDED.water_ml;
