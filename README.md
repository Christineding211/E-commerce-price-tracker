# E-Commerce Price Monitoring Data Platform (電商價格監測資料平台)

<p align="left">
  <img src="https://img.shields.io/badge/Apache%20Airflow-017CE1?style=for-the-badge&logo=Apache%20Airflow&logoColor=white" alt="Airflow">
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white" alt="GCP">
  <img src="https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/redis-%23DD0000.svg?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
</p>

> 一個以資料工程為核心的端到端專案，針對臺灣電商平台的降噪耳機價格進行自動化監測。  
> 專案涵蓋分散式資料擷取、Airflow 工作流排程、資料倉儲建模、雲端資料管線與 Looker Studio 視覺化分析。

---

## 🎯 專案目標與商業問題

電商平台價格變動頻繁，若只依靠人工查價，很難持續追蹤不同平台與不同商品之間的價格變化。

本專案希望解決以下問題：

- 哪個平台在特定商品上通常價格較低？
- 今日價格是否已接近或達到歷史最低價？
- 不同平台之間的價格差距如何變化？
- 哪些商品仍有較大的促銷空間？

---

## 🚀 專案核心亮點與展示能力

* **工作流協調與排程（Workflow Orchestration）**：使用 **Apache Airflow** 管理資料管線任務依賴、排程、自動重試與執行狀態追蹤。

* **分散式資料擷取**：透過 **CeleryExecutor** 搭配 **Redis** 任務佇列，將 momo 與 PChome 爬蟲任務分配至多個 Worker 平行執行，提升資料擷取效率。

* **容器化與叢集部署**：使用 **Docker** 封裝 Airflow、MySQL、Redis 等服務，並透過 **Docker Swarm** 管理多服務部署與 Worker 節點擴展。

* **資料倉儲與資料品質設計**：依循 **Kimball Data Warehouse** 思維設計 **Raw → Staging → Fact → Mart** 分層架構，實作資料清洗、去重、日期標準化與跨平台商品名稱匹配，提升資料一致性。

* **雲端資料管線與權限管理**：建立 **MySQL → GCS → BigQuery** 的雲端資料流程，並使用 **IAM Service Account** 與 **Docker Secret** 管理雲端憑證。


---

## 🏗️ 專案架構與資料流 (System Architecture)

<img width="729" height="304" alt="Data Pipeline" src="https://github.com/user-attachments/assets/6a2e5c7f-a11b-4a6e-b84f-e7009539693a" />

### 核心元件說明

* **Apache Airflow**：負責排程與協調整體 Data Pipeline
* **CeleryExecutor**：將爬蟲任務分散至多個 Worker 平行執行
* **Redis**：作為 Celery Message Broker，負責暫存和分派任務
* **Flower**：監控 Worker 狀態、任務執行情況與 Queue 使用狀態
* **MySQL**：實作 Raw → Staging → Fact 資料倉儲分層
* **Google Cloud Storage (GCS)**：作為 MySQL 與 BigQuery 間的資料交換層
* **BigQuery**：建立 Mart 與分析資料集，提供 Looker Studio 查詢
* **Looker Studio**：建立價格趨勢、平台價差與歷史價格分析儀表板


## 📁 專案目錄結構 (Project Structure)
```text
.
├── crawler/                 # momo 與 PChome 資料擷取模組
│   ├── config.py            # 爬蟲設定與環境參數讀取
│   └── tasks_crawler.py     # 商品資料擷取、欄位解析與資料寫入邏輯
├── dataflow/                # Airflow 工作流排程與 ETL 流程
│   ├── dags/
│   │   └── trigger_producer.py  # Airflow 主 DAG，串接資料擷取、轉換與雲端載入流程
│   └── etl/                 # Data Warehouse 分層轉換邏輯
│       ├── refresh_stg_*.py     # Staging 層：資料清洗、格式標準化與去重
│       ├── refresh_fct_daily.py # Fact 層：每日商品價格彙整與跨平台商品匹配
│       ├── export_*_to_bigquery.py # 將處理後資料匯出至 GCS 並載入 BigQuery
│       └── sql/                 # Raw → Staging → Fact 轉換 SQL
├── deploy/                  # Docker Swarm 與 GCP 部署設定
│   ├── env/                 # 環境變數樣板與設定產生工具
│   ├── local-swarm/         # 本機 Docker Swarm 部署設定
│   └── gcp-single-vm/       # GCP 單機 VM 部署設定
├── docs/                    # 專案文件、部署筆記與架構紀錄
├── scripts/                 # 連線測試與資料匯出輔助腳本
├── archived/                # 舊版架構、測試檔案與歷史實驗紀錄
├── pyproject.toml           # Python 專案依賴管理
├── uv.lock                  # uv 依賴鎖定檔
└── README.md                # 專案說明文件
```
## 📊 資料來源

本專案蒐集臺灣電商平台 **momo** 與 **PChome** 的降噪耳機商品資料，監測品牌包含：

- Sony
- Sennheiser
- JLab
- Soundcore

主要蒐集欄位包含商品名稱、商品 ID、價格、銷售資訊、來源平台與爬取時間。

## 🛠️ 技術架構

| 類別 | 使用技術 |
|---|---|
| Workflow Orchestration | Apache Airflow, CeleryExecutor |
| Data Ingestion | Python, Requests, JSON parsing |
| Database / Data Warehouse | MySQL, BigQuery, Raw / Staging / Fact / Mart |
| Containerisation | Docker, Docker Swarm |
| Message Broker / Worker | Redis, Airflow Worker |
| Cloud Platform | GCP, GCS, IAM Service Account, Docker Secret |
| Analytics | Looker Studio, SQL, Data Mart |

## 🔄 Data Pipeline 流程

Airflow DAG 負責管理完整資料流程：

```text
Scrape momo / PChome
        ↓
Load Raw Data to MySQL
        ↓
Refresh Staging Layer
        ↓
Refresh Fact Table
        ↓
Export to GCS
        ↓
Load to BigQuery
        ↓
Visualise in Looker Studio

主要流程包含：

Data Ingestion：蒐集 momo 與 PChome 商品價格資料。
Raw Layer：保留平台原始資料，支援追溯與重跑。
Staging Layer：進行資料清洗、日期標準化、價格驗證與去重。
Fact Layer：建立每日商品價格資料，支援歷史追蹤與跨平台比較。
Mart Layer：建立價格趨勢、平台價差、歷史最低價與價格警示資料集。
Cloud Analytics Layer：將資料匯出至 GCS，載入 BigQuery，並串接 Looker Studio。
