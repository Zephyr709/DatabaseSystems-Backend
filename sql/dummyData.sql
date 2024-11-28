-- Insert dummy data into subscription
DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO subscription (subscriptionType, billingCycle, startDate, renewalDate, paymentStatus)
        VALUES (
            (ARRAY['Basic', 'Pro', 'Premium'])[ceil(random() * 3)], -- Random subscription type
            (ARRAY['Monthly', 'Yearly'])[ceil(random() * 2)], -- Random billing cycle
            NOW() - (interval '1 month' * random() * 12), -- Random start date within the last year
            NOW() + (interval '1 month' * (1 + random() * 12)), -- Random renewal date within the next year
            (ARRAY['Paid', 'Pending', 'Failed'])[ceil(random() * 3)] -- Random payment status
        );
    END LOOP;
END $$;

-- Helper function for realistic first names and last names
DO $$
BEGIN
    CREATE TEMP TABLE temp_names (
        first_name TEXT,
        last_name TEXT
    );

    -- Populate with a sample of common first and last names
    INSERT INTO temp_names (first_name, last_name) VALUES
        ('John', 'Smith'),
        ('Jane', 'Doe'),
        ('Michael', 'Johnson'),
        ('Emily', 'Davis'),
        ('Chris', 'Brown'),
        ('Ashley', 'Wilson'),
        ('David', 'Miller'),
        ('Sophia', 'Taylor'),
        ('Daniel', 'Anderson'),
        ('Emma', 'Thomas'),
        ('Liam', 'Moore'),
        ('Olivia', 'Martin'),
        ('Ethan', 'Lee'),
        ('Ava', 'Clark'),
        ('Noah', 'Walker'),
        ('Isabella', 'Harris'),
        ('Mason', 'Young'),
        ('Mia', 'King'),
        ('Lucas', 'Wright'),
        ('Amelia', 'Scott');
END $$;

-- Insert dummy data into professional with realistic names
DO $$
DECLARE
    fname TEXT;
    lname TEXT;
BEGIN
    FOR i IN 1..1000 LOOP
        SELECT first_name, last_name INTO fname, lname
        FROM temp_names ORDER BY random() LIMIT 1;

        INSERT INTO professionals (name, email, maxSeats, currentSeats, subscriptionId)
        VALUES (
            fname || ' ' || lname, -- Full name
            'professional_' || i || '@example.com', -- Unique email
            (random() * 50)::int + 1, -- Max seats between 1 and 50
            (random() * 50)::int, -- Current seats between 0 and maxSeats
            (SELECT subscriptionId FROM subscription ORDER BY random() LIMIT 1) -- Random subscription
        );
    END LOOP;
END $$;

-- Insert dummy data into users with realistic names
DO $$
DECLARE
    fname TEXT;
    lname TEXT;
BEGIN
    FOR i IN 1..1000 LOOP
        SELECT first_name, last_name INTO fname, lname
        FROM temp_names ORDER BY random() LIMIT 1;

        INSERT INTO users (country, city, height, gender, weight, birthdate, email, name, nutritionGoal, macroSplit, totalLogins, lastLogin, subscriptionId, professionalId)
        VALUES (
            (ARRAY['USA', 'Canada', 'UK', 'Germany', 'France'])[ceil(random() * 5)], -- Random country
            'City_' || (random() * 1000)::int, -- Random city name
            (random() * 50 + 150)::numeric(5, 2), -- Height between 150 and 200
            (ARRAY['Male', 'Female', 'Other'])[ceil(random() * 3)], -- Random gender
            (random() * 50 + 50)::numeric(5, 2), -- Weight between 50 and 100
            NOW() - (interval '1 year' * (18 + random() * 50)), -- Random birthdate between 18 and 68 years ago
            'user_' || i || '@example.com', -- Unique email
            fname || ' ' || lname, -- Full name
            (ARRAY['Lose Weight', 'Maintain Weight', 'Gain Muscle'])[ceil(random() * 3)], -- Random nutrition goal
            (ARRAY['40/30/30', '50/30/20', '30/40/30'])[ceil(random() * 3)], -- Random macro split
            (random() * 1000)::int, -- Total logins
            NOW() - (interval '1 day' * random() * 365), -- Last login within the last year
            (SELECT subscriptionId FROM subscription ORDER BY random() LIMIT 1), -- Random subscription
            (SELECT professionalId FROM professionals ORDER BY random() LIMIT 1) -- Random professional
        );
    END LOOP;
END $$;

-- Clean up temporary table
DROP TABLE IF EXISTS temp_names;


-- Insert dummy data into metrics
DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO metrics (inputTokenUsage, outputTokenUsage, userId)
        VALUES (
            (random() * 1000)::int, -- Random input token usage
            (random() * 1000)::int, -- Random output token usage
            (SELECT userId FROM users ORDER BY random() LIMIT 1) -- Random userId
        );
    END LOOP;
END $$;

-- Insert dummy data into targets
DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO targets (calories, protein, carbs, fiber, userId)
        VALUES (
            (random() * 2000 + 1000)::int, -- Calories between 1000 and 3000
            (random() * 200)::numeric(5, 2), -- Protein up to 200g
            (random() * 300)::numeric(5, 2), -- Carbs up to 300g
            (random() * 50)::numeric(5, 2), -- Fiber up to 50g
            (SELECT userId FROM users ORDER BY random() LIMIT 1) -- Random userId
        );
    END LOOP;
END $$;

-- Insert dummy data into foodItem
DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO foodItem (name, calories, protein, carbs, fats, fiber, sugar, sodium, cholesterol)
        VALUES (
            'FoodItem_' || i, -- Name
            (random() * 300 + 50)::numeric(6, 2), -- Calories between 50 and 350
            (random() * 50)::numeric(5, 2), -- Protein up to 50g
            (random() * 100)::numeric(5, 2), -- Carbs up to 100g
            (random() * 30)::numeric(5, 2), -- Fats up to 30g
            (random() * 15)::numeric(5, 2), -- Fiber up to 15g
            (random() * 50)::numeric(5, 2), -- Sugar up to 50g
            (random() * 1000)::numeric(6, 2), -- Sodium up to 1000mg
            (random() * 500)::numeric(6, 2) -- Cholesterol up to 500mg
        );
    END LOOP;
END $$;

-- Insert dummy data into dailyMealLog
DO $$
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO dailyMealLog (mealLogId, userId, foodItemId, dateLogged)
        VALUES (
            i, -- mealLogId
            (SELECT userId FROM users ORDER BY random() LIMIT 1), -- Random userId
            (SELECT foodItemId FROM foodItem ORDER BY random() LIMIT 1), -- Random foodItemId
            NOW() - (interval '1 day' * random() * 365) -- Random date within the last year
        );
    END LOOP;
END $$;
