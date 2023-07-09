-- Create the Individuals table
CREATE TABLE individuals (
  Individual_ID VARCHAR(100) PRIMARY KEY,
  given_Name VARCHAR(100),
  surname varchar(100),
  Birth_Date varchar(100),
  Death_Date varchar(100),
  Gender CHAR(1),
  FatherID varchar(100),
  MotherID varchar(100),
  Occupation VARCHAR(100)
);

-- Create the Places table
CREATE TABLE Places (
  PlaceID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100)
);

create table families(
  family_id varchar(100) PRIMARY KEY, 
  husband_id varchar(100),
  wife_id varchar(100),
  marriage_date varchar(100),
  FOREIGN KEY (husband_id) REFERENCES individuals(Individual_ID),
  FOREIGN KEY (wife_id) REFERENCES individuals(Individual_ID)
);

-- Create the Relationships table
CREATE TABLE Relationships (
  RelationshipID INT  AUTO_INCREMENT PRIMARY KEY,
  IndividualID varchar(50),
  SpouseID varchar(50),
  MarriageDate varchar(50),
  DivorceDate varchar(50),
  FOREIGN KEY (IndividualID) REFERENCES individuals(Individual_ID),
  FOREIGN KEY (SpouseID) REFERENCES individuals(Individual_ID)
);

-- Create the Children table
CREATE TABLE Children (
  ChildID INT,
  FatherID INT,
  MotherID INT,
  FOREIGN KEY (ChildID) REFERENCES Individuals(IndividualID),
  FOREIGN KEY (FatherID) REFERENCES Individuals(IndividualID),
  FOREIGN KEY (MotherID) REFERENCES Individuals(IndividualID)
);

-- Create the Events table
CREATE TABLE Events (
  EventID INT AUTO_INCREMENT PRIMARY KEY,
  IndividualID VARCHAR(100),
  EventType VARCHAR(100),
  EventDate varchar(50),
  EventPlaceID INT,
  FOREIGN KEY (IndividualID) REFERENCES individuals(Individual_ID),
  FOREIGN KEY (EventPlaceID) REFERENCES Places(PlaceID));



  -- Create the Family Event Detail table
CREATE TABLE Family_Event_Detail (
  FamilyEventDetailID INT AUTO_INCREMENT PRIMARY KEY,
  HusbandIndividualID VARCHAR(50),
  WifeIndividualID VARCHAR(50),
  EventID INT,
  FOREIGN KEY (EventID) REFERENCES Events(EventID),
  FOREIGN KEY (HusbandIndividualID) REFERENCES individuals(Individual_ID),
  FOREIGN KEY (WifeIndividualID) REFERENCES individuals(Individual_ID)
);

-- Create the Attributes table
CREATE TABLE Attributes (
  AttributeID INT PRIMARY KEY,
  IndividualID INT,
  AttributeType VARCHAR(100),
  AttributeValue VARCHAR(255),
  FOREIGN KEY (IndividualID) REFERENCES Individuals(IndividualID)
);
