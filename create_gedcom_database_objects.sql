-- Create the Individuals table
CREATE TABLE Individuals (
  IndividualID INT PRIMARY KEY,
  Name VARCHAR(100),
  BirthDate DATE,
  DeathDate DATE,
  Gender CHAR(1),
  FatherID INT,
  MotherID INT,
  Occupation VARCHAR(100),
  UNIQUE (Name)
);

-- Create the Places table
CREATE TABLE Places (
  PlaceID INT PRIMARY KEY,
  Name VARCHAR(100)
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
  EventID INT PRIMARY KEY,
  IndividualID INT,
  EventType VARCHAR(100),
  EventDate DATE,
  EventPlaceID INT,
  FOREIGN KEY (IndividualID) REFERENCES Individuals(IndividualID),
  FOREIGN KEY (EventPlaceID) REFERENCES Places(PlaceID)
);

-- Create the Attributes table
CREATE TABLE Attributes (
  AttributeID INT PRIMARY KEY,
  IndividualID INT,
  AttributeType VARCHAR(100),
  AttributeValue VARCHAR(255),
  FOREIGN KEY (IndividualID) REFERENCES Individuals(IndividualID)
);
