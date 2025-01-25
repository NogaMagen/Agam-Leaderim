CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL,
    government_id INT UNIQUE NOT NULL
);


CREATE TABLE employers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    government_id INT UNIQUE NOT NULL
);


CREATE TABLE employees_to_employers (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    employer_id INT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE CASCADE,
    CONSTRAINT unique_employee_employer UNIQUE (employee_id, employer_id)
);
