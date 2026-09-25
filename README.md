# ☁️ Multi-Cloud FinOps & Cost Arbitrage Analytics Engine

# ☁️ Multi-Cloud FinOps & Cost Arbitrage Analytics Engine

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Multi-Cloud](https://img.shields.io/badge/Cloud-AWS%20%7C%20Azure%20%7C%20GCP-232F3E?style=for-the-badge)

An enterprise-grade financial operations (FinOps) platform that standardizes multi-cloud billing telemetry across AWS, Microsoft Azure, and Google Cloud Platform (GCP). The engine leverages unsupervised machine learning to detect underutilized "zombie" infrastructure, applies time-series regression to project short-term burn rates, and provides an executive Power BI dashboard with dynamic cross-cloud migration arbitrage modeling.

---

## 📑 Table of Contents
- [Business Problem](#-business-problem)
- [Project Objectives](#-project-objectives)
- [System Architecture](#-system-architecture)
- [Tech Stack & Dependencies](#-tech-stack--dependencies)
- [Repository Structure](#-repository-structure)
- [Data Pipeline & Machine Learning](#-data-pipeline--machine-learning)
- [Executive Power BI Dashboard](#-executive-power-bi-dashboard)
- [Future Scope](#-future-scope)
- [Author](#-author)

---

## 💼 Business Problem
Modern enterprises deploy workloads across multiple public clouds to mitigate downtime and avoid vendor lock-in. However, this creates severe financial friction:
1. **Taxonomy Discrepancy:** AWS (CUR), Azure (Cost Management), and GCP (Cloud Billing) export billing schemas with incompatible service naming conventions, metric units, and metadata structures.
2. **Idle Resource Waste:** Over-provisioned and orphaned instances ("zombie" resources) remain running, incurring substantial ongoing costs without contributing to production workloads.
3. **Forecasting Inaccuracy:** Cloud billing variability makes manual budget forecasting unreliable, often leading to unexpected overruns at quarter-end.
4. **Lack of Arbitrage Agility:** IT leaders lack dynamic modeling tools to calculate exact cost savings prior to executing compute migration across cloud providers.

---

## 🎯 Project Objectives
* **Standardize 325,000+ Raw Ingestion Records:** Clean, reshape, and normalize disparate billing schemas into a unified Star Schema data model.
* **Unsupervised Anomaly Identification:** Deploy an Isolation Forest algorithm to systematically identify compute instances generating high run costs against negligible utilization.
* **Predictive Run-Rate Forecasting:** Engineer time-series lag features and train a Random Forest Regressor to forecast daily cloud expenditures for the upcoming 7 days.
* **Accelerated High-Volume Loading:** Utilize SQLAlchemy alongside `fast_executemany` bulk insertion to load 300K+ enterprise records into Microsoft SQL Server within seconds.
* **Commercial Arbitrage Modeling:** Deliver an interactive executive Power BI dashboard complete with What-If parameter controls simulating provider cost arbitrage.

---

## 🏗️ System Architecture

```text
+-----------------------+      +-----------------------+      +-----------------------+
|  AWS CUR Ingestion   |      |  Azure Billing Export |      |   GCP Cloud Billing   |
| (120,000 Raw Records) |      | (110,000 Raw Records) |      |  (95,000 Raw Records) |
+-----------+-----------+      +-----------+-----------+      +-----------+-----------+
            |                              |                              |
            +------------------------------+------------------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |       Pandas Vectorized ETL Engine    |
                       | - Master Taxonomy Cross-Mapping       |
                       | - Fast Regex Tag Attribute Extraction |
                       | - CostPerUnit Feature Derivation      |
                       +-------------------+-------------------+
                                           |
                   +-----------------------+-----------------------+
                   |                                               |
                   v                                               v
   +-------------------------------+               +-------------------------------+
   |   Scikit-Learn ML Engine      |               |  SQLAlchemy Bulk Data Loader  |
   | - Isolation Forest (Zombies)  |               | - Fast Execute Many Protocol  |
   | - Random Forest (7-Day Spend) |               | - Schema Genesis & Star Schema|
   +---------------+---------------+               +---------------+---------------+
                   |                                               |
                   +-----------------------+-----------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |    Microsoft SQL Server Data Mart     |
                       | - Fact_CloudSpend (325K Records)      |
                       | - Dim_ZombieResources                 |
                       | - Fact_CostForecast                   |
                       +-------------------+-------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |     Executive Power BI Console        |
                       | - DAX Multi-Cloud Run-Rate Measures   |
                       | - What-If Migration Arbitrage Slider  |
                       | - Priority Zombie Decommission Matrix |
                       +---------------------------------------+

An enterprise-grade financial operations (FinOps) platform that standardizes multi-cloud billing telemetry across AWS, Microsoft Azure, and Google Cloud Platform (GCP). The engine leverages unsupervised machine learning to detect underutilized "zombie" infrastructure, applies time-series regression to project short-term burn rates, and provides an executive Power BI dashboard with dynamic cross-cloud migration arbitrage modeling.
```
---

### 📑 Table of Contents
- [Business Problem](#-business-problem)
- [Project Objectives](#-project-objectives)
- [System Architecture](#-system-architecture)
- [Tech Stack & Dependencies](#-tech-stack--dependencies)
- [Repository Structure](#-repository-structure)
- [Data Pipeline & Machine Learning](#-data-pipeline--machine-learning)
- [Executive Power BI Dashboard](#-executive-power-bi-dashboard)
- [Future Scope](#-future-scope)

---

## 💼 Business Problem
Modern enterprises deploy workloads across multiple public clouds to mitigate downtime and avoid vendor lock-in. However, this creates severe financial friction:
1. **Taxonomy Discrepancy:** AWS (CUR), Azure (Cost Management), and GCP (Cloud Billing) export billing schemas with incompatible service naming conventions, metric units, and metadata structures.
2. **Idle Resource Waste:** Over-provisioned and orphaned instances ("zombie" resources) remain running, incurring substantial ongoing costs without contributing to production workloads.
3. **Forecasting Inaccuracy:** Cloud billing variability makes manual budget forecasting unreliable, often leading to unexpected overruns at quarter-end.
4. **Lack of Arbitrage Agility:** IT leaders lack dynamic modeling tools to calculate exact cost savings prior to executing compute migration across cloud providers.

---

## 🎯 Project Objectives
* **Standardize 325,000+ Raw Ingestion Records:** Clean, reshape, and normalize disparate billing schemas into a unified Star Schema data model.
* **Unsupervised Anomaly Identification:** Deploy an Isolation Forest algorithm to systematically identify compute instances generating high run costs against negligible utilization.
* **Predictive Run-Rate Forecasting:** Engineer time-series lag features and train a Random Forest Regressor to forecast daily cloud expenditures for the upcoming 7 days.
* **Accelerated High-Volume Loading:** Utilize SQLAlchemy alongside `fast_executemany` bulk insertion to load 300K+ enterprise records into Microsoft SQL Server within seconds.
* **Commercial Arbitrage Modeling:** Deliver an interactive executive Power BI dashboard complete with What-If parameter controls simulating provider cost arbitrage.

---

## 🏗️ System Architecture

```text
+-----------------------+      +-----------------------+      +-----------------------+
|  AWS CUR Ingestion   |      |  Azure Billing Export |      |   GCP Cloud Billing   |
| (120,000 Raw Records) |      | (110,000 Raw Records) |      |  (95,000 Raw Records) |
+-----------+-----------+      +-----------+-----------+      +-----------+-----------+
            |                              |                              |
            +------------------------------+------------------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |       Pandas Vectorized ETL Engine    |
                       | - Master Taxonomy Cross-Mapping       |
                       | - Fast Regex Tag Attribute Extraction |
                       | - CostPerUnit Feature Derivation      |
                       +-------------------+-------------------+
                                           |
                   +-----------------------+-----------------------+
                   |                                               |
                   v                                               v
   +-------------------------------+               +-------------------------------+
   |   Scikit-Learn ML Engine      |               |  SQLAlchemy Bulk Data Loader  |
   | - Isolation Forest (Zombies)  |               | - Fast Execute Many Protocol  |
   | - Random Forest (7-Day Spend) |               | - Schema Genesis & Star Schema|
   +---------------+---------------+               +---------------+---------------+
                   |                                               |
                   +-----------------------+-----------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |    Microsoft SQL Server Data Mart     |
                       | - Fact_CloudSpend (325K Records)      |
                       | - Dim_ZombieResources                 |
                       | - Fact_CostForecast                   |
                       +-------------------+-------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |     Executive Power BI Console        |
                       | - DAX Multi-Cloud Run-Rate Measures   |
                       | - What-If Migration Arbitrage Slider  |
                       | - Priority Zombie Decommission Matrix |
                       +---------------------------------------+
```
---
## 🛠️ Tech Stack & Dependencies

* **ETL & Data Processing:** Python 3.12 (Pandas, NumPy) for vectorized transformations and regex extraction.
* **Machine Learning:** Scikit-Learn (`IsolationForest` for anomaly detection, `RandomForestRegressor` for time-series forecasting).
* **Data Warehousing:** Microsoft SQL Server, SQLAlchemy, and `pyodbc` for automated schema compilation and bulk execution.
* **Business Intelligence:** Microsoft Power BI and DAX for dimensional modeling and dynamic What-If parameters.

### Python Environment Dependencies
```bash
pip install pandas numpy scikit-learn sqlalchemy pyodbc
```
---
## 📂 Repository Structure

```text
📦 Multi-Cloud-FinOps-Arbitrage-Engine
 ┣ 📜 FinOps_SQL.sql            # Creating Databases and verify the tables and row counts.
 ┣ 📜 data_generator.py         # Synthesizes 325,000+ realistic raw multi-cloud billing records
 ┣ 📜 etl_pipeline.py           # Normalization engine mapping AWS, Azure, & GCP taxonomies
 ┣ 📜 ml_engine.py              # ML workflows for zombie asset detection & time-series spend forecasting
 ┣ 📜 sql_loader.py             # Optimized SQLAlchemy bulk data loader for MS SQL Server
 ┣ 📜 zombie_resources.csv      # Model output: Identified idle cloud resources prioritized by waste
 ┣ 📜 cost_forecast.csv         # Model output: 7-day forward-looking predictive spend projections
 ┣ 📜 FinOps_Dashboard.pbix     # Power BI data model, DAX library, and interactive executive interface
 ┗ 📜 README.md                 # Complete system documentation
```
---
## 🚀 Future Scope

* **Automated Cloud Provider API Connectors:** Replace static billing CSV ingestion with real-time extraction via the AWS Cost Explorer API, Azure Consumption API, and Google Cloud Billing API.
* **Automated Decommission Webhooks:** Link the Zombie Decommission Matrix directly to AWS Systems Manager / Azure Automation runbooks to stop idle instances automatically via webhook approvals.
* **Container-Level Allocation (Kubernetes FinOps):** Ingest Kubecost metrics to break down compute expenditures to granular Kubernetes namespaces and Pod deployments.
* **Modern Cloud Lakehouse Migration:** Transition the database storage layer from MS SQL Server to Microsoft Fabric / Azure Synapse using Delta Parquet tables.
