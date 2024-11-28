-- Supabase AI is experimental and may produce incorrect answers
-- Always verify the output before executing

create table if not exists
  items (
    id bigint primary key generated always as identity,
    name text not null
  );

insert into
  items (name)
values
  ('Item One');

insert into
  items (name)
values
  ('Item Two');

select
  *
from
  items;

create table
  subscription (
    subscriptionId bigint primary key generated always as identity,
    subscriptionType text not null, -- Type of subscription (e.g., "Basic", "Pro", etc.)
    billingCycle text not null, -- Billing cycle (e.g., "Monthly", "Yearly")
    startDate timestamp with time zone not null, -- Start date of the subscription
    renewalDate timestamp with time zone not null, -- Renewal date for the subscription
    paymentStatus text not null -- Payment status (e.g., "Paid", "Pending", "Failed")
    --foreign key (userId) references users(userId), -- Foreign key referencing the user table
    --foreign key (professionalId) references professional(professionalId) -- Foreign key referencing the professional table
  );

create table
  professionals (
    professionalId bigint primary key generated always as identity,
    name text not null,
    email text unique not null,
    maxSeats integer not null, -- Maximum number of clients the professional can manage
    currentSeats integer not null default 0, -- Number of clients currently managed (default to 0)
    --foreign key (subscriptionId) references subscription (subscriptionId) -- Foreign key referencing the subscription table
    subscriptionId bigint,
    FOREIGN KEY (subscriptionId) REFERENCES subscription (subscriptionId) on delete set null
  );

create table
  users (
    userId bigint primary key generated always as identity,
    country text not null,
    city text not null,
    height numeric(5, 2) not null,
    gender text not null,
    weight numeric(5, 2) not null,
    birthdate timestamp with time zone not null,
    email text unique not null,
    name text not null,
    nutritionGoal text not null,
    macroSplit text not null,
    totalLogins integer default 0 not null,
    lastLogin timestamp,
    createdAt timestamp default current_timestamp not null, -- Timestamp when the record was created
    subscriptionId bigint, -- Foreign key to the subscription table (optional for the user)
    professionalId bigint, -- Foreign key to the professional table (optional for the user)
    FOREIGN KEY (subscriptionId) REFERENCES subscription (subscriptionId) on delete set null, -- Foreign key to subscription table
    FOREIGN KEY (professionalId) REFERENCES professionals (professionalId) on delete set null -- Foreign key to professional table
  );

create table
  metrics (
    metricsId bigint primary key generated always as identity, -- Unique identifier for each entry
    inputTokenUsage integer not null, -- Number of tokens used for input processing
    outputTokenUsage integer not null, -- Number of tokens used for output processing
    userId bigint,
    foreign key (userId) references users (userId) on delete cascade -- Foreign key linking to the subscription table's userID
  );

create table
  targets (
    targetId bigint primary key generated always as identity,
    calories integer,
    protein numeric(5, 2),
    carbs numeric(5, 2),
    fiber numeric(5, 2),
    userId bigint,
    foreign key (userId) references users (userId) on delete cascade -- Foreign key linking to the subscription table's userID
  );

create table
  foodItem (
    foodItemId bigint primary key generated always as identity, -- Auto-incrementing primary key
    name text not null, -- Name of the food item (up to 255 characters)
    calories numeric(6, 2) not null, -- Calories (up to 9999.99)
    protein numeric(5, 2) not null, -- Protein content in grams (up to 999.99)
    carbs numeric(5, 2) not null, -- Carbohydrates content in grams (up to 999.99)
    fats numeric(5, 2) not null, -- Fat content in grams (up to 999.99)
    fiber numeric(5, 2) not null, -- Fiber content in grams (up to 999.99)
    sugar numeric(5, 2) not null, -- Sugar content in grams (up to 999.99)
    sodium numeric(6, 2) not null, -- Sodium content in milligrams (up to 9999.99)
    cholesterol numeric(6, 2) not null -- Cholesterol content in milligrams (up to 9999.99)
  );

CREATE TABLE dailyMealLog (
    mealLogId BIGINT,
    userId BIGINT,
    foodItemId BIGINT,
    dateLogged TIMESTAMP WITH TIME ZONE NOT NULL, -- Date when the meal was logged
    
    PRIMARY KEY (mealLogId, foodItemId, userId), -- Composite primary key
    
    -- Foreign key references
    FOREIGN KEY (userId) REFERENCES users (userId) on delete cascade,
    FOREIGN KEY (foodItemId) REFERENCES foodItem (foodItemId) on delete cascade
);
  



  


