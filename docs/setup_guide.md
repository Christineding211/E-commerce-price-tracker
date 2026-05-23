# Environment

     Ubuntu

#### install uv

    curl -LsSf https://astral.sh/uv/install.sh | sh

#### install Python 3.11

    uv python install 3.11

#### set uv venv

    uv venv --python 3.11


uv init

uv sync

#### 建立環境變數

    ENV=DEV python genenv.py
    ENV=DOCKER python genenv.py

 
# Worker

#### 啟動預設執行 celery 的 queue 的工人

    uv run celery -A crawler.worker worker --loglevel=info
    uv run --env-file=.env celery -A crawler.worker worker --loglevel=info

#### 啟動執行 pchome_q 的 momo_q 的工人

#pchome
    uv run celery -A crawler.worker worker -Q pchome_q -c 4 --hostname=celery@%h --loglevel=info
    uv run --env-file=.env celery -A crawler.worker worker -Q pchome_q -c 4 --hostname=celery@%h --loglevel=info

#momo
    uv run celery -A crawler.worker worker -Q momo_q -c 1 --hostname=celery@%h --loglevel=info
    uv run --env-file=.env celery -A crawler.worker worker -Q momo_q -c 1 --hostname=celery@%h --loglevel=info
    
# Producer

#### 發送任務

    uv run python crawler/producer.py
    uv run --env-file=.env python crawler/producer.py

#### 發送任務到不同 queue

    uv run python crawler/producer_multi_queue.py
    uv run --env-file=.env python crawler/producer_multi_queue.py


## Docker Compose 檔案說明


### 基礎設施（要先啟動）

| 檔案 | 啟動什麼 | 說明 |
| --- | --- | --- |
| `rabbitmq.yml` | RabbitMQ + Flower | 本地開發用，使用 `dev` 網路。Flower 是 Celery 的監控 Web UI（port 5555） |
| `rabbitmq-network.yml` | RabbitMQ + Flower | 正式環境版本，使用外部 `dev_network ` 網路，讓多個 compose 檔能共用網路 |
| `mysql.yml` | MySQL 8.0 + phpMyAdmin | MySQL 在 3306，phpMyAdmin 在 8000（瀏覽器可視化管理 DB） |

### Worker（消費者，執行爬蟲）

| 檔案 | 說明 |
| --- | --- |
| `docker-compose-worker.yml` | 單一 worker，使用 `dev` 網路，最簡單的版本 |
| `docker-compose-worker-network.yml` | 起兩個 worker（momo_q, pchome_q），各自監聽不同 queue，使用 `dev_network` | 用 `DOCKER_IMAGE_VERSION` 環境變數指定，方便切換版本 |

### Producer（生產者，派送任務）

| 檔案 | 說明 |
| --- | --- |
| `docker-compose-producer-network.yml` | 執行 `producer_multi_queue.py`，一次性派送任務到 pchome/momo queue |
| 同上，image 版本可透過環境變數指定 |
| `docker-compose-producer-duplicate-network-version.yml` | 執行去重複版本的 producer |


### 注意事項

檔名看起來很長，其實有規則：
- 使用外部 `dev_network`（需要先 `docker network create my_network`），讓不同 compose 檔之間能互通
- **`-version`**：image 版本改用 `${DOCKER_IMAGE_VERSION}` 變數，啟動時要搭配 `DOCKER_IMAGE_VERSION=v5 docker compose up -d`
- 每次改過code 都要重新build image `docker build -f Dockerfile -t my-crawler:v8 .` 然後去.env 檔新增`‵DOCKER_IMAGE_VERSION=v9` 再用這個版本加在worker , producer 啟動前面


### 典型啟動順序

```bash
# 1. 建立共用網路（只要做一次）
docker network create dev_network

# 2. 啟動基礎設施
docker compose -f rabbitmq-network.yml up -d
docker compose -f mysql.yml up -d

# 3. 啟動 workers
DOCKER_IMAGE_VERSION=v8 docker compose -f docker-compose-worker-network.yml up -d

#派送任務
DOCKER_IMAGE_VERSION=v8 docker compose -f docker-compose-producer-network.yml up -d

# 4. 啟動 scheduler（自動派送任務）
DOCKER_IMAGE_VERSION=0.0.6 docker compose -f docker-compose-scheduler-network-version.yml up -d

# 5. 打開 http://localhost:5555 看 Flower 監控 worker 狀態
# 6. 打開 http://localhost:8000 用 phpMyAdmin 看 MySQL 資料

