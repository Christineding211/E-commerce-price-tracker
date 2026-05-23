# Docker

#### build docker image

    docker build -f Dockerfile -t my-crawler:v1 .
    docker build -f Dockerfile -t my-crawler:v2 .
    docker build -f Dockerfile -t my-crawler:v3 .
    docker build -f Dockerfile -t my-crawler:v5 .
    docker build -f Dockerfile -t my-crawler:v8 .
    

    docker build -f with.env.Dockerfile -t my-crawler:v9 .
    docker build -f with.env.Dockerfile -t  my-crawler:v10 .


#### push docker image

#docker hub create respositories:e-commerce-crawler

docker tag my-crawler:v10 christine0211/e-commerce-crawler:v10 
docker push christine0211/e-commerce-crawler:v10


#### 建立 network

    docker network create dev_network

#### 啟動 rabbitmq

    docker compose -f rabbitmq-network.yml up -d

#### 關閉 rabbitmq

    docker compose -f rabbitmq-network.yml down

#### 啟動 mysql

    docker compose -f mysql.yml up -d

#### 關閉 mysql

    docker compose -f mysql.yml down

#### 啟動 worker

    docker compose -f docker-compose-worker-network.yml up -d

   DOCKER_IMAGE_VERSION=v5 docker compose -f docker-compose-worker-network.yml up -d
   DOCKER_IMAGE_VERSION=v6 docker compose -f docker-compose-worker-network.yml up -d
   DOCKER_IMAGE_VERSION=v8 docker compose -f docker-compose-worker-network.yml up -d
   DOCKER_IMAGE_VERSION=v9 docker compose -f docker-compose-worker-network.yml up -d

#### 關閉 worker

    docker compose -f docker-compose-worker-network.yml down
    DOCKER_IMAGE_VERSION=v5 docker compose -f docker-compose-worker-network-version.yml down
    DOCKER_IMAGE_VERSION=v6 docker compose -f docker-compose-worker-network-version.yml down
    DOCKER_IMAGE_VERSION=v8 docker compose -f docker-compose-worker-network-version.yml down

#### producer 發送任務

    docker compose -f docker-compose-producer-network.yml up -d
    DOCKER_IMAGE_VERSION=v6 docker compose -f docker-compose-producer-network.yml up -d
    DOCKER_IMAGE_VERSION=v8 docker compose -f docker-compose-producer-network.yml up -d
    DOCKER_IMAGE_VERSION=v9 docker compose -f docker-compose-producer-network.yml up -d

#### 查看 docker container 狀況

    docker ps -a

#### 查看 log

    docker logs container_name