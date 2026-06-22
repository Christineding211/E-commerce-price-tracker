# E-Commerce Price Monitoring Data Platform  
# 電商價格監測資料平台

> 一個以資料工程為核心的端到端專案，針對臺灣電商平台的降噪耳機價格進行自動化監測。  
> 專案涵蓋分散式資料擷取、Airflow 工作流排程、資料倉儲建模、雲端資料管線與 Looker Studio 視覺化分析。

---

## 1. 專案簡介

本專案建立一套電商價格監測資料平台，自動蒐集 **momo** 與 **PChome** 的降噪耳機商品價格資料，並將原始資料整理成可分析、可追蹤、可視覺化的資料集。

整體流程涵蓋：

```text
資料擷取 → 資料清洗 → 資料倉儲 → 雲端儲存 → BigQuery → Looker Studio
```

此專案重點不只是爬蟲，而是展示如何將分散的電商商品資料，透過資料工程流程轉換為穩定、可維護且可支援商業分析的資料平台。

---

## 2. 專案目標與商業問題

電商平台價格變動頻繁，若只依靠人工查價，很難持續追蹤不同平台與不同商品之間的價格變化。

本專案希望解決以下問題：

- 哪個平台在特定商品上通常價格較低？
- 今日價格是否已接近或達到歷史最低價？
- 不同平台之間的價格差距如何變化？
- 哪些商品仍有較大的促銷空間？
- 如何建立一套可每日自動更新的價格監測流程？

---

## 3. 專案展示能力

本專案主要展示以下資料工程能力：

- 使用 **Apache Airflow** 進行工作流排程與任務管理
- 使用 **CeleryExecutor** 與 Worker Queue 建立分散式資料擷取流程
- 使用 **Docker** 與 **Docker Swarm** 進行多服務容器化部署
- 設計 **Raw → Staging → Fact → Mart** 四層資料倉儲架構
- 實作資料清洗、去重、日期標準化與跨平台商品匹配
- 建立 **MySQL → GCS → BigQuery** 雲端資料管線
- 使用 **Looker Studio** 建立價格趨勢與平台價差分析報表

---

## 4. 資料來源

本專案蒐集臺灣兩個主要電商平台的商品資料：

- momo
- PChome

監測商品類別為降噪耳機，品牌包含：

- Sony
- Sennheiser
- JLab
- Soundcore

蒐集欄位包含：

- 商品名稱
- 商品 ID
- 商品價格
- 銷售資訊
- 來源平台
- 爬取時間

---

## 5. 技術架構

### Data Engineering

- Python
- SQL
- Apache Airflow
- CeleryExecutor
- Redis
- MySQL
- Docker
- Docker Swarm

### Cloud Platform

- Google Cloud Platform（GCP）
- Google Cloud Storage（GCS）
- BigQuery
- IAM Service Account
- Docker Secret

### Analytics

- Looker Studio
- Data Warehouse
- Data Mart
- 價格趨勢分析
- 平台價差分析

---

## 6. 系統架構

```text
                    ┌────────────────────┐
                    │  Apache Airflow     │
                    │  DAG Orchestration  │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ CeleryExecutor      │
                    │ Distributed Workers │
                    └─────────┬──────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
      ┌──────────────┐                ┌───────────────┐
      │ momo crawler │                │ PChome crawler│
      └──────┬───────┘                └──────┬────────┘
             │                               │
             └───────────────┬───────────────┘
                             ▼
                    ┌────────────────────┐
                    │ MySQL              │
                    │ Raw / Staging /    │
                    │ Fact tables        │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Google Cloud        │
                    │ Storage             │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ BigQuery            │
                    │ Mart tables         │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Looker Studio       │
                    │ Dashboard           │
                    └────────────────────┘
```

---

## 7. Data Pipeline 流程

Airflow DAG 負責管理完整資料流程：

```text
start
  ↓
爬取 momo 與 PChome 商品資料
  ↓
寫入 MySQL Raw Layer
  ↓
更新 Staging Layer
  ↓
更新 Fact Table
  ↓
匯出資料至 Google Cloud Storage
  ↓
載入 BigQuery
  ↓
提供 Looker Studio 視覺化分析
```

主要階段如下：

1. **Data Ingestion**：透過 Python 爬蟲蒐集 momo 與 PChome 商品資料。
2. **Raw Layer**：保留平台原始資料，方便追溯來源與重新處理。
3. **Staging Layer**：進行資料清洗、日期標準化、價格格式驗證與去重。
4. **Fact Layer**：建立每日商品價格事實表，支援歷史價格追蹤與跨平台比較。
5. **Mart Layer**：建立分析用資料集，例如價格趨勢、平台價差、歷史最低價與價格警示。
6. **Cloud Analytics Layer**：將處理後資料匯出至 GCS，再載入 BigQuery，最後串接 Looker Studio 進行視覺化分析。

---

## 8. Data Warehouse 設計

本專案採用分層式資料倉儲設計：

```text
Raw → Staging → Fact → Mart
```

### Raw Layer

儲存 momo 與 PChome 的原始爬蟲資料。

用途：

- 保留原始來源資料
- 支援資料追溯
- 方便未來重新清洗或調整轉換邏輯

### Staging Layer

針對原始資料進行清洗與標準化。

處理邏輯包含：

- 日期標準化
- 價格格式驗證
- 移除重複資料
- 統一平台欄位格式
- 每日每商品保留一筆有效資料

### Fact Layer

建立每日商品價格事實表。

用途：

- 儲存每日商品價格
- 支援歷史價格追蹤
- 支援 momo 與 PChome 跨平台價格比較

### Mart Layer

建立商業分析導向的資料集。

範例：

- 商品價格時間序列
- 每日最佳價格
- 平台價差分析
- 今日價格警示表

---

## 9. 商品匹配與資料品質

不同平台對同一個商品的命名方式可能不同，例如：

```text
Sony WH-1000XM5
Sony WH1000XM5 Black
索尼 WH-1000XM5 降噪耳機
```

因此本專案建立商品維度表，透過關鍵字匹配方式，將不同平台商品名稱對應到統一的官方商品型號。

資料品質處理包含：

- 使用 SQL Window Function 進行去重
- 標準化日期與平台欄位
- 驗證價格欄位格式
- 建立商品名稱匹配規則
- 統一跨平台商品維度

---

## 10. 分析指標與輸出

### Product Price Timeline

追蹤不同商品在 momo 與 PChome 的每日價格變化。

### Platform Price Difference

比較同一商品在不同平台上的價格差異。

### Historical Low Price Tracking

追蹤目前價格是否接近或等於歷史最低價。

### Price Buffer

衡量目前價格與歷史最低價之間的距離。

```text
Price Buffer = (今日價格 - 歷史最低價) / 歷史最低價
```

Price Buffer 越高，代表目前價格距離歷史低點越遠，可能仍有較大的促銷空間。

---

## 11. 專案結構

```text
.
├── crawler/                 # momo 與 PChome 爬蟲邏輯
├── dataflow/                # Airflow DAG、SQL 腳本與資料流程
├── deploy/                  # Docker Swarm 部署設定
├── docs/                    # 專案文件與架構說明
├── scripts/                 # 工具腳本
├── archived/                # 歷史版本與舊架構檔案
├── pyproject.toml           # Python 專案依賴
├── uv.lock                  # uv lock file
└── README.md
```

---

## 12. 部署方式

本專案使用 Docker Swarm 進行容器化部署。

主要服務包含：

- Airflow Webserver
- Airflow Scheduler
- Airflow Worker
- Redis
- MySQL
- Flower
- phpMyAdmin

Google Cloud 憑證管理方式：

- IAM Service Account
- Docker Secret
- `GOOGLE_APPLICATION_CREDENTIALS`

雲端資料管線會將 MySQL 中的資料匯出至 GCS，並載入 BigQuery 供 Looker Studio 使用。

---

## 13. 為什麼使用 Airflow，而不是另外撰寫 scheduler.py？

本專案使用 **Apache Airflow** 作為工作流排程與任務管理工具。

因此每日自動化流程由 Airflow DAG Scheduler 管理，而不是額外撰寫 `scheduler.py`。

Airflow 負責：

- 排程資料管線
- 管理任務依賴
- 自動重試失敗任務
- 紀錄任務執行狀態
- 追蹤任務 Log
- 協調分散式 Worker 執行任務

這樣可以讓資料流程更容易維護、監控與擴充。

---

## 14. 未來優化方向

未來可持續擴充以下功能：

- 新增更多電商平台
- 使用 Embedding Similarity 改善商品匹配
- 增加價格異常偵測
- 建立自動化價格警示通知
- 將 Worker 部署至多台 VM
- 改善增量載入策略
- 建立 CI/CD 部署流程

---

## 15. 專案總結

本專案展示如何從原始電商資料出發，建立一套完整的資料工程流程。

涵蓋內容包含：

- Apache Airflow 工作流排程
- 分散式資料擷取
- Docker Swarm 容器化部署
- MySQL 資料倉儲設計
- GCS 與 BigQuery 雲端資料整合
- Looker Studio 商業分析視覺化

本專案的核心價值在於將原始、分散且格式不一致的電商商品資料，轉換為穩定、可追蹤且可支援商業分析的資料集。
