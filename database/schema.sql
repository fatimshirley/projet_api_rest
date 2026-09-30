cleCREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
email VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_id
ON users (id);

CREATE INDEX IF NOT EXISTS ix_users_email
ON users (email);

CREATE TABLE IF NOT EXISTS tasks (
id SERIAL PRIMARY KEY,
title VARCHAR(200) NOT NULL,
description TEXT NULL,
priority VARCHAR(10) NOT NULL,
completed BOOLEAN NOT NULL DEFAULT FALSE,
user_id INTEGER NOT NULL,
created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,


CONSTRAINT fk_tasks_user
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE,

CONSTRAINT chk_tasks_priority
    CHECK (priority IN ('low', 'medium', 'high'))


);

CREATE INDEX IF NOT EXISTS ix_tasks_id
ON tasks (id);

CREATE INDEX IF NOT EXISTS ix_tasks_user_id
ON tasks (user_id);
