create or replace function get_user_by_userid (s_userid bigint) 
returns table (
  country text,
  city text,
  height numeric,
  gender text,
  weight numeric,
  birthdate timestamp,
  email text,
  name text,
  nutritiongoal text,
  macrosplit text,
  totallogins int,
  lastlogin timestamp,
  createdat timestamp,
  subscriptionid bigint,
  professionalid bigint
) as $$
BEGIN
  RETURN QUERY SELECT * FROM users WHERE users.userid = s_userid;
END;
$$

--DROP FUNCTION get_user_by_userid(bigint)


CREATE OR REPLACE FUNCTION get_user_by_userid(s_userid bigint) 
RETURNS TABLE (LIKE users)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM users WHERE users.userid = s_userid;
END;
$$
 LANGUAGE plpgsql;