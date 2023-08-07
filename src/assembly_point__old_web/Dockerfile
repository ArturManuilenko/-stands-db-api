FROM gitlab.neroelectronics.by:5050/unic-lab/system/docker-images/basic-python:1.3.0

WORKDIR /docker_app

COPY Pipfile /docker_app/Pipfile
COPY Pipfile.lock /docker_app/Pipfile.lock
RUN export PYTHONPATH
RUN pipenv install --dev --system

COPY ./src/assembly_point__old_web /docker_app/src/assembly_point__old_web
RUN chmod -R +x ./src/assembly_point__old_web/cgi_bin/
