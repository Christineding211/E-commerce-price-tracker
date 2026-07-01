# Docker

#### build docker image

docker build -f deploy/local-swarm/with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.19 .

docker build -f deploy/local-swarm/with.env.Dockerfile_Airflow -t christine0211/e-commerce-airflow:0.0.20 .

#### push docker image
docker push christine0211/e-commerce-airflow:0.0.19
docker push christine0211/e-commerce-airflow:0.0.20

# Airflow  (Docker Swarm)

#### deploy airflow stack
docker stack deploy --with-registry-auth -c deploy/local-swarm/docker-compose-airflow.yml airflow
docker stack deploy -c deploy/local-swarm/docker-compose-airflow.yml airflow
