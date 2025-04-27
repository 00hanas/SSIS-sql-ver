CREATE DATABASE ssis;
USE ssis;

CREATE TABLE college (
	collegeCode VARCHAR(10) PRIMARY KEY,
    collegeName VARCHAR(100) NOT NULL
);

CREATE TABLE program (
	programCode VARCHAR(20) PRIMARY KEY,
    programName VARCHAR(100) NOT NULL,
    collegeCode VARCHAR(10), 
    FOREIGN KEY (collegeCode) REFERENCES college(collegeCode)
);


CREATE TABLE student (
	studentID VARCHAR(9) PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    yearLevel INT CHECK (yearLevel BETWEEN 1 AND 5),
    gender ENUM('Male', 'Female'),
    programCode VARCHAR(20),
    FOREIGN KEY (programCode) REFERENCES program(programCode)
);


select USER()

