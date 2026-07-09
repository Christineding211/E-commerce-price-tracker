# E-Commerce Price Monitoring Data Platform

<p align="right">
  <strong>🇬🇧 English</strong> | <a href="./README.zh-TW.md">🇹🇼 繁體中文</a>
</p>

<p align="left">
  <img src="https://img.shields.io/badge/Apache%20Airflow-017CE1?style=for-the-badge&logo=Apache%20Airflow&logoColor=white" alt="Airflow">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white" alt="GCP">
  <img src="https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/redis-%23DD0000.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
</p>

> An end-to-end data engineering project for monitoring the prices of noise-cancelling headphones across Taiwan's two major e-commerce platforms, Momo and PChome.
>
> Built with Apache Airflow, Docker, MySQL, GCS and BigQuery, the platform collects, transforms and models pricing data into data marts for historical price tracking, cross-platform price comparison and Looker Studio dashboards.

This project addresses a common retail challenge: tracking competitor pricing across multiple e-commerce platforms without relying on manual price checks.



---

## 🎯 Business Questions

E-commerce prices change frequently, making it difficult to track price movements manually across platforms, brands and products.

This project aims to answer the following questions:

- Which platform usually offers a lower price for a specific product?
- Is today's price close to, or equal to, the historical lowest price?
- How does the price difference between platforms change over time?
- Which products still have room for further discounts or promotions?

---

## 🚀 Key Highlights

- **Workflow Orchestration**: Used Apache Airflow to manage task dependencies, scheduling and pipeline execution.

- **Distributed Data Ingestion**: Used CeleryExecutor with Redis to distribute Momo and PChome scraping tasks across multiple workers for parallel execution.

- **Containerisation and Deployment**: Containerised Airflow, MySQL and Redis with Docker, and used Docker Swarm to manage multi-service deployment.

- **Data Warehouse Design**: Designed a Kimball-style Raw → Staging → Fact → Mart model with deduplication, date standardisation and product matching.

- **Cloud Data Pipeline**: Built a MySQL → GCS → BigQuery data pipeline, using an IAM Service Account and Docker Secret for secure credential management.

---

## 🏗️ System Architecture

<img width="729" height="304" alt="Data Pipeline" src="https://github.com/user-attachments/assets/6a2e5c7f-a11b-4a6e-b84f-e7009539693a" />

### Core Components

- **Apache Airflow**: Orchestrates and schedules the overall data pipeline.
- **CeleryExecutor**: Distributes scraping tasks across multiple workers.
- **Redis**: Acts as the Celery message broker for task queuing and distribution.
- **Flower**: Monitors worker status, task execution and queue usage.
- **MySQL**: Stores Raw, Staging and Fact layer data.
- **Google Cloud Storage (GCS)**: Acts as the intermediate storage layer between MySQL and BigQuery.
- **BigQuery**: Stores analytical marts and reporting datasets.
- **Looker Studio**: Provides dashboards for price trends, platform price differences and historical price analysis.

---

## 📁 Project Structure

```text
.
├── crawler/                 # Data ingestion modules for Momo and PChome
│   ├── config.py            # Crawler configuration and environment variable loading
│   └── tasks_crawler.py     # Product scraping, field parsing and database insertion logic
├── dataflow/                # Airflow workflows and ETL processes
│   ├── dags/
│   │   └── trigger_producer.py  # Main Airflow DAG
│   └── etl/                 # Data warehouse transformation logic
│       ├── refresh_stg_*.py
│       ├── refresh_fct_daily.py
│       ├── export_*_to_bigquery.py
│       └── sql/
├── deploy/                  # Docker Swarm and GCP deployment configuration
│   ├── env/
│   ├── local-swarm/
│   └── gcp-single-vm/
├── docs/                    # Project documentation and deployment notes
├── scripts/                 # Helper scripts
├── archived/                # Legacy architecture and experiments
├── pyproject.toml
├── uv.lock
└── README.md
```

## 📊 Data Sources
The monitored brands include:

Sony,
Sennheiser,
JLab,
Soundcore

The main fields collected include product name, product ID, price, sales information, source platform and scraping timestamp.

## 🛠️ Technical Stack
| Category                  | Technologies                                 |
| ------------------------- | -------------------------------------------- |
| Workflow Orchestration    | Apache Airflow, CeleryExecutor               |
| Data Ingestion            | Python, Requests, JSON parsing               |
| Database / Data Warehouse | MySQL, BigQuery, Raw / Staging / Fact / Mart |
| Containerisation          | Docker, Docker Swarm                         |
| Message Broker / Worker   | Redis, Airflow Worker                        |
| Cloud Platform            | GCP, GCS, IAM Service Account, Docker Secret |
| Analytics                 | Looker Studio, SQL, Data Mart                |

## 🔄 Data Pipeline
The Airflow DAG manages the full data pipeline:
```text
Scrape momo / PChome
        ↓
Load raw data into MySQL
        ↓
Refresh Staging layer
        ↓
Refresh Fact table
        ↓
Export to GCS
        ↓
Load into BigQuery
        ↓
Visualise in Looker Studio

```

The main pipeline stages are:

- Data Ingestion: Collects product price data from Momo and PChome.
- Raw Layer: Stores platform-level raw data for traceability and reprocessing.
- Staging Layer: Cleans data, standardises dates, validates prices and removes duplicates.
- Fact Layer: Builds daily product price records for historical tracking and cross-platform comparison.
- Mart Layer: Creates datasets for price trends, platform price differences, historical lowest prices and price monitoring.
- Cloud Analytics Layer: Exports processed data to GCS, loads it into BigQuery and connects it to Looker Studio.

## 🗄️Data Warehouse Design

This project uses a layered data warehouse design:
```text
┌─────────────┐
│    Raw      │
│ Source Data │
└──────┬──────┘
       │
┌──────▼──────┐
│  Staging    │
│ Clean &     │
│ Standardise │
└──────┬──────┘
       │
┌──────▼──────┐
│    Fact     │
│ Daily Price │
└──────┬──────┘
       │
┌──────▼──────┐
│    Mart     │
│ Analytics   │
└─────────────┘
```
The purpose of this structure is to separate raw source data from cleaned, standardised and analysis-ready datasets. This improves traceability, data quality and the ability to rerun specific parts of the pipeline when needed.

## ✅ Data Quality and Product Matching
The same product may appear under different names across platforms, such as `Sony WH-1000XM5`, `Sony WH1000XM5 Black` 

To support reliable cross-platform comparison, I created a product dimension table and used rule-based keyword matching to map platform-specific names to standard product models.

Data quality checks include:

- Deduplication using SQL window functions
- Date, platform and price standardisation
- Cross-platform product matching
- Consistent product dimensions for price comparison and historical tracking

  ## 📈 Analytics Outputs
  The Mart layer converts the Fact table into reporting-ready datasets for business analysis and dashboarding.

It supports the following analytical outputs:

Product Price Trend Analysis: Tracks daily price movements for each product across Momo and PChome.
Historical Low Price Monitoring: Identifies whether today's price is equal to or lower than the historical lowest price.
Price Buffer Analysis: Measures how far the current price is from the historical lowest price.
Cross-platform Price Difference Analysis: Compares the same product across platforms to identify price advantages.

```text

Price Buffer = (Current Price - Historical Lowest Price) / Historical Lowest Price

Price Difference % = (momo_price - pchome_price) / pchome_price * 100
```
Dashboard Preview
<!-- Replace this with your Looker Studio dashboard screenshot --> <img width="900" alt="Looker Studio Dashboard" src="YOUR_DASHBOARD_IMAGE_URL" />

## 🔮 Future Improvements
Expand to more e-commerce platforms and product categories.
Introduce embedding-based matching to improve product matching quality.
Support horizontal scaling across multiple VM workers.
Build price anomaly detection and notification mechanisms.
Add CI/CD automation for deployment.
