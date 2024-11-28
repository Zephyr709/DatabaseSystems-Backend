CREATE ROLE it_user;
CREATE ROLE it_admin;
SELECT rolname FROM pg_roles; --view created roles

GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO it_admin;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO it_user;

-- Automatically grant permissions for any new tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT INSERT, UPDATE, DELETE ON TABLES TO it_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO it_user;


UPDATE users
SET role = 'it_user'
WHERE ID = 'e3214d27-9405-4d9e-ad80-705341002ca1';

SELECT * FROM users WHERE role IS NOT NULL;


CREATE TABLE account_roles (
  id SERIAL PRIMARY KEY,          -- Unique ID for each role
  user_id UUID NOT NULL,          -- Foreign key to the user
  role_name TEXT NOT NULL,        -- The role assigned to the user
  created_at TIMESTAMP DEFAULT NOW(), -- Timestamp for role assignment
  UNIQUE (user_id, role_name)     -- Ensure no duplicate roles per user
);

INSERT INTO account_roles (user_id, role_name)
VALUES ('e3214d27-9405-4d9e-ad80-705341002ca1', 'it_user');


SELECT 
    grantee, 
    table_catalog, 
    table_schema, 
    table_name, 
    privilege_type
FROM 
    information_schema.role_table_grants
WHERE 
    grantee = 'it_admin';

ALTER TABLE professional ENABLE ROW LEVEL SECURITY;

SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'professional';

SELECT relname AS table_name, relrowsecurity AS rls_enabled
FROM pg_class
WHERE relname = 'professional';
