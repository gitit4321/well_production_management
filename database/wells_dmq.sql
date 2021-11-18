-- Michael Hilmes and Paul Owen
-- Project Group 27 - 
-- CS340 Step 4 - Data Manipulation Queries

------------------
-- Wells --
------------------

-- Default lookup for Wells
SELECT well_id, company_id, basin_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells ORDER BY well_id;

-- Add new Well
INSERT INTO Wells(company_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date) VALUES
	(:company_id, :formation_id, :total_production_bbls, :1st_prod_date, :last_prod_date);

-- Search for Well
SELECT well_id, company_id, formation_id, total_production_bbls, 1st_prod_date, last_prod_date FROM Wells WHERE company_id = :company_id_input;

-- Update Well
UPDATE Wells SET
	company_id = :company_id_input,
	formation_id = :formation_id_input, 
	total_production_bbls = :total_production_bbls_input, 
	1st_prod_date = :1st_prod_date_input,
	last_prod_date = :last_prod_date_input
WHERE
	well_id = :well_id_input;

-- DELETE Well
DELETE FROM Wells WHERE company_id = :company_id_input;

------------------
-- Basins --
------------------

-- Default lookup for Basins
SELECT basin_id, basin_name, total_wells, total_formations, total_production_bbls FROM Basins ORDER BY basin_id;

-- Add new Basin
INSERT INTO Basin(basin_name, total_wells, total_formations, total_production_bbls) VALUES
	(:basin_name, :total_wells, :total_formations, :total_production_bbls);

-- Update Basin
UPDATE Basin SET
	basin_name = :basin_name_input, 
	total_wells = :total_wells_input,
	total_formations = :total_formations_input,
	total_production_bbls = :total_production_bbls_input
WHERE
	basin_id = :basin_id_input;

------------------
-- Formations --
------------------

-- Default lookup for Formations
SELECT formation_id, formation_name, basin_id, total_wells, total_production_bbls FROM Formations ORDER BY formation_id;

-- Add new Formation
INSERT INTO Formation(formation_name, basin_id, total_wells, total_production_bbls) VALUES
	(:formation_name, :basin_id, :total_wells, :total_production_bbls);

-- Update Formation
UPDATE Formation SET
	formation_name = :formation_name_input, 
	basin_id = :basin_id_input,
	total_wells = :total_wells_input,
	total_production_bbls = :total_production_bbls_input
WHERE
	formation_id = :formation_id_input;

------------------
-- Companies --
------------------

-- Default lookup for Companies
SELECT company_id, company_name, total_wells, total_production_bbls, total_basins, total_formations FROM Companies ORDER BY company_id;

-- Add new Company
INSERT INTO Companies(company_name, total_wells, total_production_bbls, total_basins, total_formations) VALUES
	(:company_name, :total_wells, :total_production_bbls, :total_basins, :total_formations);

-- Update Company
UPDATE Companies SET
	company_name = :company_name_input, 
	total_wells = :total_wells_input, 
	total_production_bbls = :total_production_bbls_input,
	total_basins = :total_basins_input,
	total_formations = :total_formations_input
WHERE
	company_id = :company_id_input;

-- DELETE Company
DELETE FROM Companies WHERE company_id = :company_id_input;

------------------
-- Basins_Operators --
------------------

-- Default lookup for Basins_Operators
SELECT basin_id, company_id FROM Basins_Operators ORDER BY basin_id;

-- Add Basins_Operators
INSERT INTO Basins_Operators(basin_id, company_id) VALUES (:basin_id, :company_id);

-- Update Basins_Operators
UPDATE Basins_Operators SET
	company_id = :company_id_input,
	formation_id = :formation_id_input;

------------------
-- Operators_Formations --
------------------

-- Default lookup for Operators_Formations
SELECT company_id, formation_id FROM Basins_Operators ORDER BY basin_id;

-- Add Operator_Formation
INSERT INTO Operators_Formations(company_id, formation_id) VALUES (:company_id, :formation_id);

-- Update Operator_Formation
UPDATE Operators_Formations SET
	company_id = :company_id_input,
	formation_id = :formation_id_input;