FROM library/nginx:1.19-alpine

COPY ./src/assembly_point__balancer/remote /etc/nginx

WORKDIR /docker_app

COPY ./src/assembly_point__web/static /docker_app/assembly_point__web/static
