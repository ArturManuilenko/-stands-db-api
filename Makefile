SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

nothing:
	@echo "do nothing"

up:
	docker-compose up --remove-orphans --build \
		assembly_point__balancer \
		assembly_point__api \
		assembly_point__web \
		assembly_point__old_web\

check_env:
	@./srv/check_env.sh

cleanup:
	docker login gitlab.neroelectronics.by:5050 -u unic_lab_developers -p Vw3o4gBzgH_GGUzFs7NM

	@# git submodule foreach "git fetch && git merge origin/dev"
	git submodule init
	git submodule update --remote
	pipenv sync --dev

	ulpytool install

lint:
	pipenv run lint

tests:
	pipenv run test

drop:
	docker-compose down -v

fix_own:
	@echo "me: $(ME)"
	sudo chown $(ME):$(ME) -R .

######################## MANAGER STANDS API DB START ########################

assembly_point__db__dump:
	docker-compose run --rm manager__assembly_point__db uldbutls dump '--db-uri=$$ASSEMBLY_POINT__DB_URI'

assembly_point__db__migrate:
	docker-compose run --rm manager__assembly_point__db uldbutls migrate --app-dir="./src/assembly_point__db"

assembly_point__db__revision:
	docker-compose run --rm manager__assembly_point__db uldbutls revision --app-dir="./src/assembly_point__db"

assembly_point__db__init:
	docker-compose run --rm manager__assembly_point__db uldbutls init --app-dir="./src/assembly_point__db"

assembly_point__db__upgrade:
	docker-compose run --rm manager__assembly_point__db uldbutls upgrade --app-dir="./src/assembly_point__db"

assembly_point__db__downgrade:
	docker-compose run --rm manager__assembly_point__db uldbutls downgrade --app-dir="./src/assembly_point__db"

######################## MANAGER STANDS API DB END ##########################
