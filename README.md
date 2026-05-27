# E-commerce-price-tracker

# Docker

#### build docker image

    docker build -f with.env.Dockerfile_Airflow -t my-crawler:v11 .
    docker build -f with.env.Dockerfile_Airflow -t my-crawler_dataflow:0.0.1 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.2 .
    docker build -f with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.3 .

#### push docker image
    -- docker tag my-crawler_dataflow:0.0.1 christine0211/e-commerce-crawler:airflow-0.0.1
    docker push christine0211/e-commerce-crawler:airflow-0.0.1
    docker push christine0211/e-commerce-airflow:0.0.2 
    docker push christine0211/e-commerce-airflow:0.0.3
    





# Airflow 部署 (Docker Swarm)

#### deploy airflow stack

    DOCKER_IMAGE_VERSION=v11 docker stack deploy -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=airflow-0.0.1 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.2 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow
    DOCKER_IMAGE_VERSION=0.0.3 docker stack deploy --with-registry-auth -c docker-compose-airflow.yml airflow



    

#### 移除 airflow stack

    docker stack rm airflow