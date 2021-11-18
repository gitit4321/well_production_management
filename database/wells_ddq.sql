-- Michael Hilmes and Paul Owen
-- Project Group 27 - 
-- CS340 Step 4 - Data Definition Queries + Sample Data

DROP TABLE IF EXISTS Basins;
CREATE TABLE Basins (
	basin_id INT(11) NOT NULL AUTO_INCREMENT,
	basin_name VARCHAR(255) NOT NULL,
	total_wells INT(11),
	total_formations INT(11),
	total_production_bbls INT(11),
	PRIMARY KEY (basin_id)
) ENGINE=InnoDB;

INSERT INTO Basins (basin_name, total_wells, total_formations, total_production_bbls) VALUES
    ('Midland', NULL, NULL, NULL), 
    ('Delaware', NULL, NULL, NULL),
    ('Gulf Coast', NULL, NULL, NULL);

DROP TABLE IF EXISTS Companies;
CREATE TABLE Companies (
	company_id INT(11) NOT NULL AUTO_INCREMENT,
	company_name VARCHAR(255) NOT NULL,
	total_wells INT(11),
	total_production_bbls INT(11),
	total_basins INT(11),
	total_formations INT(11),
	PRIMARY KEY (company_id)
) ENGINE=InnoDB;

INSERT INTO Companies (company_name, total_wells, total_production_bbls, total_basins, total_formations) VALUES
    ('Ovintiv', NULL, NULL, NULL, NULL), 
    ('XTO', NULL, NULL, NULL, NULL),
    ('Devon', NULL, NULL, NULL, NULL),
    ('Concho', NULL, NULL, NULL, NULL);

DROP TABLE IF EXISTS Formations;
CREATE TABLE Formations (
    formation_id INT(11) NOT NULL AUTO_INCREMENT,
    formation_name VARCHAR(255) NOT NULL,
    basin_id INT(11) NOT NULL,
    total_wells INT(11),
    total_production_bbls INT(11),
    PRIMARY KEY (formation_id),
    FOREIGN KEY (basin_id) REFERENCES Basins(basin_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO Formations (formation_name, basin_id, total_wells, total_production_bbls) VALUES
    ('Eagle Ford', 1, NULL, NULL), 
    ('Wolfcamp A', 2, NULL, NULL),
    ('Bone Spring', 3, NULL, NULL);

DROP TABLE IF EXISTS Wells;
CREATE TABLE Wells (
    well_id INT(11) AUTO_INCREMENT,
    company_id INT(11),
    basin_id INT(11) NOT NULL,
    formation_id INT(11) NOT NULL,
    total_production_bbls INT(11),
    1st_prod_date DATE NOT NULL,
    last_prod_date DATE,
    PRIMARY KEY (well_id),
    FOREIGN KEY (company_id) REFERENCES Companies(company_id)  ON DELETE CASCADE,
    FOREIGN KEY (basin_id) REFERENCES Basins(basin_id) ON DELETE CASCADE,
    FOREIGN KEY (formation_id) REFERENCES Formations(formation_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO Wells (company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date) VALUES
    ((SELECT company_id FROM Companies WHERE company_name = 'Ovintiv'),
        (SELECT basin_id FROM Basins WHERE basin_name = 'Gulf Coast'),
        (SELECT formation_id FROM Formations WHERE formation_name = 'Eagle Ford'),
        ('120000'), 
        ('2018-01-20')),
    ((SELECT company_id FROM Companies WHERE company_name = 'XTO'),
        (SELECT basin_id FROM Basins WHERE basin_name = 'Midland'),
        (SELECT formation_id FROM Formations WHERE formation_name = 'Wolfcamp A'),
        ('200400'), 
        ('2017-07-06')),
    ((SELECT company_id FROM Companies WHERE company_name = 'Devon'),
        (SELECT basin_id FROM Basins WHERE basin_name = 'Delaware'),
        (SELECT formation_id FROM Formations WHERE formation_name = 'Bone Spring'),
        ('175000'), 
        ('2016-11-04'));

DROP TABLE IF EXISTS Basins_Operators;
CREATE TABLE Basins_Operators (
    basin_id INT(11) NOT NULL,
    company_id INT(11) NOT NULL,
    FOREIGN KEY (basin_id) REFERENCES Basins(basin_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO Basins_Operators (basin_id, company_id) VALUES
    ((SELECT basin_id FROM Basins WHERE basin_name = 'Gulf Coast'),
        (SELECT company_id FROM Companies WHERE company_name = 'Ovintiv')),
    ((SELECT basin_id FROM Basins WHERE basin_name = 'Midland'),
        (SELECT company_id FROM Companies WHERE company_name = 'XTO')),
    ((SELECT basin_id FROM Basins WHERE basin_name = 'Delaware'),
        (SELECT company_id FROM Companies WHERE company_name = 'Devon'));

DROP TABLE IF EXISTS Operators_Formations;
CREATE TABLE Operators_Formations (
    company_id INT(11) NOT NULL,
    formation_id INT(11) NOT NULL,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id) ON DELETE CASCADE,
    FOREIGN KEY (formation_id) REFERENCES Formations (formation_id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO Operators_Formations (company_id, formation_id) VALUES
    ((SELECT company_id FROM Companies WHERE company_name = 'Ovintiv'),
        (SELECT formation_id FROM Formations WHERE formation_name = 'Eagle Ford')),
    ((SELECT company_id FROM Companies WHERE company_name = 'XTO'),
        (SELECT formation_id FROM Formations WHERE formation_name = 'Wolfcamp A')),
    ((SELECT company_id FROM Companies WHERE company_name = 'Devon'),
        (SELECT formation_id FROM Formations WHERE formation_name = 'Bone Spring'));
