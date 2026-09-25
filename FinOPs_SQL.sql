CREATE DATABASE EnterpriseFinOps;
GO

--Verify the tables and row counts
USE EnterpriseFinOps;
GO

--Check 'Fact_Cloud table'
Select * from Fact_CloudSpend

--Check 'Dim_ZombieResources'
Select * from Dim_ZombieResources

--Check 'Fact_CostForecast table'
Select * from Fact_CostForecast


SELECT 
    'Fact_CloudSpend' AS TableName, COUNT(*) AS Row_Count FROM Fact_CloudSpend
UNION ALL
SELECT 
    'Dim_ZombieResources', COUNT(*) FROM Dim_ZombieResources
UNION ALL
SELECT 
    'Fact_CostForecast', COUNT(*) FROM Fact_CostForecast;

Select * from Fact_CloudSpend