CREATE TABLE IF NOT EXISTS kotiki (
  id uuid NOT NULL DEFAULT (gen_random_uuid()),
  name varchar(255) NOT NULL,
  PRIMARY KEY (id)
);