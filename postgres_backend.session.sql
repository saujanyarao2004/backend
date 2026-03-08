/*CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) CHECK (role IN ('patient','doctor','admin')) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);*/

/*CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50)UNIQUE NOT NULL
);*/

/*ALTER TABLE users
ADD COLUMN role_id INT REFERENCES roles(role_id);*/

/*INSERT INTO roles (role_name)
VALUES
('PATIENT'),
('DOCTOR'),
('ADMIN');
*/

/*SELECT *
FROM roles;

SELECT 
    users.user_id,
    users.email,
    users.role_id
FROM
    users;
*/

/*ALTER TABLE users
DROP COLUMN name;*/

/*CREATE TABLE patients(
    patient_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT CHECK (age>=0),
    gender VARCHAR(10),
    contact_number VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_patient_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);*/

/*CREATE TABLE patient_health_info(
    health_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    blood_group VARCHAR(3),
    blood_presseure_status VARCHAR(20),
    diabetes_status VARCHAR(20),
    allergies TEXT,
    disablities TEXT,
    previous_health_history TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_health_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);*/

/*ALTER TABLE patient_health_info
    ADD COLUMN  height INT,
    ADD COLUMN  weight INT,
    ADD COLUMN  age INT,
    ADD COLUMN  blood_group VARCHAR(3);*/

/*CREATE TABLE doctors(
    doctor_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE,
    hospital_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_doctor_user
    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);*/

/*ALTER TABLE doctors
    ADD COLUMN  age INT,
    ADD COLUMN  years_of_experience INT;
*/    

/*CREATE TABLE consents(
    consent_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,

    status VARCHAR(20) DEFAULT 'PENDING'
        CHECK(status IN('PENDING','ACTIVE','REVOKED')),
        

    otp_code VARCHAR(10),
    otp_expires_at TIMESTAMP,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP,

    CONSTRAINT fk_consent_patient
    FOREIGN KEY (patient_id)
    REFERENCES patients(patient_id)
    ON DELETE CASCADE,

    CONSTRAINT fk_consent_doctor
    FOREIGN KEY (doctor_id)
    REFERENCES doctors(doctor_id)
    ON DELETE CASCADE,

    CONSTRAINT unique_doctor_patient
        UNIQUE(patient_id,doctor_id)
);*/

/*CREATE TABLE medical_records(
    record_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,

    diagnosis TEXT,
    notes TEXT,
    treatment_plan TEXT,

    visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_record_patient
    FOREIGN KEY (patient_id)
    REFERENCES patients(patient_id)
    ON DELETE CASCADE,

    CONSTRAINT fk_record_doctor
    FOREIGN KEY (doctor_id)
    REFERENCES doctors(doctor_id)
    ON DELETE SET NULL 
);*/

/*ALTER TABLE medical_records
DROP COLUMN notes;
*/

/*ALTER TABLE medical_records
DROP COLUMN diagnosis,
DROP COLUMN treatment_plan;
*/

/*CREATE TABLE medical_files(
    file_id SERIAL PRIMARY KEY,
    patient_id INT NOT NULL,
    record_id INT NULL,

    uploaded_by VARCHAR(20) NOT NULL
        CHECK(uploaded_by IN('PATIENT','DOCTOR')),
    file_name VARCHAR(255) NOT NULL,
    file_tpe VARCHAR(50),
    file_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_file_patient
    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id)
    ON DELETE CASCADE,

    CONSTRAINT fk_file_record
    FOREIGN KEY (record_id)
    REFERENCES medical_records(record_id)
    ON DELETE SET NULL
);*/

/*CREATE TABLE audit_logs(
    log_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_audit_user
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    );*/

/*CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,

    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,

    appointment_date TIMESTAMP NOT NULL,

    status VARCHAR(20) DEFAULT 'UPCOMING',
    reason VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_patient
        FOREIGN KEY(patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_doctor
        FOREIGN KEY(doctor_id)
        REFERENCES doctors(doctor_id)
        ON DELETE CASCADE
);*/

/*CREATE TABLE vitals (
    vital_id SERIAL PRIMARY KEY,

    patient_id INTEGER NOT NULL,

    weight DECIMAL(5,2),
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    blood_sugar INTEGER,

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vitals_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);
*/

/*CREATE TABLE reminders (
    reminder_id SERIAL PRIMARY KEY,

    patient_id INTEGER NOT NULL,

    title VARCHAR(100) NOT NULL,
    description TEXT,

    reminder_time TIMESTAMP NOT NULL,

    status VARCHAR(20) DEFAULT 'PENDING',
    -- PENDING | COMPLETED | CANCELLED

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reminder_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);*/

/*CREATE TABLE health_profiles (
    profile_id SERIAL PRIMARY KEY,

    patient_id INTEGER NOT NULL,

    blood_group VARCHAR(5),

    allergies TEXT,

    has_disability BOOLEAN DEFAULT FALSE,
    disability_details TEXT,

    existing_diseases TEXT,

    medical_history TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_health_profile_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);*/

    








