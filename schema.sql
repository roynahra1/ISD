CREATE TABLE appointment (
    Appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE,
    Time TIME,
    Notes TEXT,
    Car_plate VARCHAR(20)
);

CREATE TABLE appointment_service (
    Appointment_id INT,
    Service_id INT,
    PRIMARY KEY (Appointment_id, Service_id)
);

CREATE TABLE services (
    Service_id INT PRIMARY KEY,
    Service_type VARCHAR(50),
    Description TEXT,
    Estimated_Duration INT
);