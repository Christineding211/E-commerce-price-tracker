# E-commerce-price-tracker

# Docker

#### build docker image

    docker build -f with.env.Dockerfile_Airflow -t my-crawler:v11 .
    docker build -f with.env.Dockerfile_Airflow -t my-crawler_dataflow:0.0.1 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.2 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.3 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.4 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.5 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.6 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.7 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.8 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.9 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.10 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.11 .
    #0.0.12 = 第一個正式 Airflow-only 版本
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.12 .

#### push docker image
    -- docker tag my-crawler_dataflow:0.0.1 christine0211/e-commerce-crawler:airflow-0.0.1
    docker push christine0211/e-commerce-crawler:airflow-0.0.1
    docker push christine0211/e-commerce-airflow:0.0.2 
    docker push christine0211/e-commerce-airflow:0.0.3
    docker push christine0211/e-commerce-airflow:0.0.4
    docker push christine0211/e-commerce-airflow:0.0.5
    docker push christine0211/e-commerce-airflow:0.0.6
    docker push christine0211/e-commerce-airflow:0.0.7
    docker push christine0211/e-commerce-airflow:0.0.8
    docker push christine0211/e-commerce-airflow:0.0.9
    docker push christine0211/e-commerce-airflow:0.0.10
    docker push christine0211/e-commerce-airflow:0.0.11
    docker push christine0211/e-commerce-airflow:0.0.12
    





# Airflow 部署 (Docker Swarm)

#### deploy airflow stack

    DOCKER_IMAGE_VERSION=v11 docker stack deploy -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=airflow-0.0.1 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.2 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.3 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.4 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.5 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.6 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.7 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.8 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.9 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.10 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.11 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.12 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    


    

#### 移除 airflow stack

    docker stack rm airflow


# GCP deploy

## Portainer
http://127.0.0.1:9000

## create-mysql-volume:
	docker volume create mysql

## remove-network
	docker network rm my_swarm_network

## create-network:
	docker network create --scope=swarm --driver=overlay my_swarm_network
	docker network create --scope=swarm --driver=overlay --attachable my_swarm_network

## deploy-docker swarm:
    docker stack deploy -c deploy/gcp-single-vm/portainer.yml por

## deploy-mysql:
    docker stack deploy --with-registry-auth -c deploy/gcp-single-vm/mysql.yml mysql


## deploy-rabbitmq:
