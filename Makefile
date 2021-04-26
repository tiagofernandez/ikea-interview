#!make
-include .env
export

ifeq (, $(shell which python3))
    $(error "Please install Python 3: https://www.python.org/downloads")
endif

ifeq (, $(shell which yarn))
    $(error "Please install Yarn: https://classic.yarnpkg.com/en/docs/install")
endif

IMAGE := warehouse-server
TAG := latest

define HELP

Usage:
    make help                  show available commands

    make init                  initialize project
    make install               download and install dependencies
    make clean                 remove object files and cached files
    make build                 compile packages and dependencies
    make run                   run the main program
    make run-api               run the api server in dev mode
    make run-web               run the web application in dev mode

    make shell                 start a python repl
    make format                format the source code
    make lint                  run lint inspections
    make test                  run unit tests
    make cover                 run test coverage checks
    make cover-report          generate test coverage report

	make docker-clean          prune stopped containers and dangling images
	make docker-image          build the docker image
	make docker-run            launch a detached container
	make docker-run-shell      launch an interactive container
	make docker-debug          debug the running container
	make docker-stop           stop the detached container
endef

export HELP

.PHONY: venv

default: help

help:
	@echo "$$HELP"

venv:
ifeq (, $(VIRTUAL_ENV))
	$(error "Please activate your virtual environment.")
endif

init:
	pip install --upgrade virtualenv
	virtualenv -p python3 venv
	cp .env.dev .env

install: venv
	pip install -r requirements-dev.txt
	pre-commit install
	cd web && yarn install

clean:
	find . -type f -name '*.pyc' -delete

build:
	cd web && yarn build

run: venv migrate build static
	gunicorn -b 0.0.0.0:5000 warehouse:app

run-api: venv
	flask run --host=0.0.0.0 --no-debugger

run-web:
	cd web && yarn start

shell: venv
	ipython

format: venv
	black warehouse --exclude="migrations"
	cd web && yarn format

lint: venv
	flake8 warehouse
	cd web && yarn lint

test: venv
	python -m pytest --capture=no

cover: venv
	python -m pytest --cov=warehouse

docker-clean:
	docker system prune -f

docker-image: build
	docker build --rm=true --squash -t $(IMAGE):$(TAG) .

docker-run:
	docker run --restart=always -p 5000:5000 -d $(IMAGE):$(TAG)

docker-run-shell:
	docker run -p 5000:5000 -ti $(IMAGE):$(TAG) /bin/sh

docker-debug:
	docker exec -ti $(shell docker ps | grep $(IMAGE):$(TAG) | awk '{print $$1}') /bin/sh

docker-stop:
	docker stop $(shell docker ps | grep $(IMAGE):$(TAG) | awk '{print $$1}')
