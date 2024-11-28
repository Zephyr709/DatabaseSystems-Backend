CREATE OR REPLACE FUNCTION get_users_by_professional(professional_id bigint)
RETURNS TABLE(
    user_id bigint,
    name text,
    email text,
    country text,
    city text
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.userId,
        u.name,
        u.email,
        u.country,
        u.city
    FROM users u
    WHERE u.professionalId = professional_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_users_by_prof_id(prof_id BIGINT)
RETURNS TABLE (LIKE users)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM users WHERE professionalid = prof_id;
END;
$$
 LANGUAGE plpgsql;

create or replace function delete_professional(prof_id bigint)
returns void as $$
begin
  delete from professional
  where professionalid = prof_id;
end;
$$ language plpgsql;


CREATE OR REPLACE FUNCTION get_subscriptions()
RETURNS TABLE(
    subscriptionid BIGINT,
    subscriptiontype TEXT,
    billingcycle TEXT,
    startdate TIMESTAMPTZ,
    renewaldate TIMESTAMPTZ,
    paymentstatus TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT subscriptionid, subscriptiontype, billingcycle, startdate, renewaldate, paymentstatus
    FROM subscription;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_users()
RETURNS TABLE (
    userid bigint,
    country text,
    city text,
    height numeric(5,2),
    gender text,
    weight numeric(5,2),
    birthdate timestamp with time zone,
    email text,
    name text,
    nutritiongoal text,
    macrosplit text,
    totallogins integer,
    lastlogin timestamp,
    createdat timestamp,
    subscriptionid bigint,
    professionalid bigint
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        "userId",
        "country",
        "city",
        "height",
        "gender",
        "weight",
        "birthdate",
        "email",
        "name",
        "nutritionGoal",
        "macroSplit",
        "totalLogins",
        "lastLogin",
        "createdAt",
        "subscriptionId",
        "professionalId"
    FROM "users";
END;
$$ LANGUAGE plpgsql;

-- SQL function to get all professionals
-- SQL function to get all professionals with lowercase attributes
create or replace function get_professionals()
returns table (
  professionalid bigint,
  name text,
  email text,
  maxseats integer,
  currentseats integer,
  subscriptionid bigint
) language plpgsql as $$
begin
  return query
  select 
    professionalid,
    name,
    email,
    maxseats,
    currentseats,
    subscriptionid
  from professional;
end;
$$;

-- SQL function to get all daily meal logs with lowercase attributes
create or replace function get_daily_meal_logs()
returns table (
  meallogid bigint,
  userid bigint,
  fooditemid bigint,
  datelogged timestamp with time zone
) language plpgsql as $$
begin
  return query
  select 
    meallogid,
    userid,
    fooditemid,
    datelogged
  from dailyMealLog;
end;
$$;

create or replace function get_metrics()
returns table (
  metricsid bigint,
  inputtokenusage integer,
  outputtokenusage integer,
  userid bigint
) language plpgsql as $$
begin
  return query
  select 
    metricsid,
    inputtokenusage,
    outputtokenusage,
    userid
  from metrics;
end;
$$;

CREATE OR REPLACE FUNCTION fetch_sorted_data(
    sort_column TEXT,
    sort_direction TEXT DEFAULT 'ASC'
) RETURNS TABLE (id INT, name TEXT, professionalid UUID, ...) AS $$
BEGIN
    RETURN QUERY EXECUTE format(
        'SELECT * FROM your_table ORDER BY %I %s',
        sort_column,
        CASE WHEN sort_direction ILIKE 'DESC' THEN 'DESC' ELSE 'ASC' END
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sort_table(
    table_name TEXT,
    sort_column TEXT,
    sort_order TEXT
) RETURNS SETOF RECORD AS  -- Use RECORD here
$$
DECLARE
    query TEXT;
BEGIN
    -- Construct the SQL query dynamically
    query := format(
        'SELECT * FROM %I ORDER BY %I %s',
        table_name, sort_column, sort_order
    );
    
    -- Execute the dynamic query and return the result
    RETURN QUERY EXECUTE query;
END;
$$ LANGUAGE plpgsql;


