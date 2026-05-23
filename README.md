# E-commerce-price-tracker

# Docker

#### build docker image

    docker build -f with.env.Dockerfile_Airflow -t my-crawler:v11 .

#### push docker image




# Airflow 部署 (Docker Swarm)

#### deploy airflow stack

    DOCKER_IMAGE_VERSION=v11 docker stack deploy -c docker-compose-airflow.yml airflow


    

#### 移除 airflow stack

    docker stack rm airflow