alter table users
drop constraint users_professionalid_fkey,
add constraint users_professionalid_fkey foreign key (professionalid) references professional (professionalid) on delete set null;


ALTER TABLE users
DROP CONSTRAINT users_professionalid_fkey;

ALTER TABLE users
ADD CONSTRAINT users_professionalid_fkey
FOREIGN KEY (professionalId) REFERENCES professional (professionalId)
ON DELETE SET NULL;
