CREATE OR REPLACE FUNCTION check_and_add_user()
RETURNS TRIGGER AS
$$
BEGIN
    -- Check if the professional has reached their seat limit
    IF (SELECT currentseats FROM professional WHERE professionalid = NEW.professionalid) >= 
       (SELECT maxseats FROM professional WHERE professionalid = NEW.professionalid) THEN
        -- If the professional has no more seats available, raise an exception
        RAISE EXCEPTION 'Professional has reached their maximum number of clients.';
    ELSE
        -- If there is space, increment currentseats and allow the user to be added
        UPDATE professional
        SET currentseats = currentseats + 1
        WHERE professionalid = NEW.professionalid;
        RETURN NEW;  -- Allow the user to be inserted
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER before_user_insert
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION check_and_add_user();

-- Function to decrement currentSeats when a user is deleted
CREATE OR REPLACE FUNCTION decrement_professional_seats()
RETURNS TRIGGER AS
$$
BEGIN
    -- Decrement currentSeats for the professional associated with the deleted user
    UPDATE professional
    SET currentseats = currentseats - 1
    WHERE professionalid = OLD.professionalid;

    RETURN OLD; -- Allow the deletion to proceed
END;
$$
LANGUAGE plpgsql;

-- Trigger to call the function before a user is deleted
CREATE TRIGGER before_user_delete
BEFORE DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION decrement_professional_seats();

CREATE OR REPLACE FUNCTION set_datelogged_to_now()
RETURNS TRIGGER AS $$
BEGIN
    NEW.dateLogged := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_datelogged_trigger
BEFORE INSERT ON dailyMealLog
FOR EACH ROW
EXECUTE FUNCTION set_datelogged_to_now();