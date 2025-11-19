.DEFAULT_GOAL := show-help

include .env
export

# BuildKit is a newer+faster docker build backend (default on Windows/Mac, available since 2018)
# see e.g. https://pythonspeed.com/articles/docker-buildkit/
# you can disable BuildKit by building as follows:
#  $ make build/... buildkit=0
buildkit = 1

# In case of error, that is hidden by the default build output, you can enable a more verbose output by
#  $ make build/... progress=plain
progress = plain  # auto|plain|tty

DOCKER_BUILD = DOCKER_BUILDKIT=${buildkit} docker build --progress=${progress}
CURRENT_DATE = $(shell date -u "+%y%m%d")
GITHASH ?= $(shell git rev-parse --short HEAD)

define HELP_TEXT
Guide for \`make\` targets:

  General:
    make show-help                      - Show this help text.
    make rm-docker                      - Clean up unused Docker resources (containers, networks, etc.).

  Talonify BE Services: Build & Run (Local Testing):
    make talonify_be_services/build     - Build the Docker image: talonify-be-services-dev for deploy.
    make talonify_be_services/build-dev - Build the Docker image: talonify-be-services-dev for development/testing.
    make talonify_be_services/run           - Run services using docker-compose.yml.
    make talonify_be_services/stop          - Stop the services defined in docker-compose.yml.

  Build and Push to AWS ECR:
    make talonify_be_services/build         - Build Docker image for API using BuildKit (tagged with ENVIRONMENT).
	
endef
export HELP_TEXT


.PHONY: show-help
show-help:
	@echo "$$HELP_TEXT"


.PHONY: rm-docker
rm-docker:
	docker system prune --force | true


.PHONY: talonify_be_services/build-dev
talonify_be_services/build-dev:
	docker build --progress=plain --build-arg REQUIREMENTS=requirements.txt -t talonify-be-services-dev:latest -f Dockerfile .


.PHONY: talonify_be_services/run
talonify_be_services/run: rm-docker talonify_be_services/build-dev
	@bash -c '\
		cleanup() { \
			echo "[Ctrl or Cmd] + C! Gracefully stopping and Cleaning up..."; \
			make talonify_be_services/stop; \
			exit 0; \
		}; \
		trap cleanup SIGINT; \
		DOCKER_REPO_NAME=db-services-dev DOCKER_DEFAULT_IMAGE_TAG=latest docker-compose -f docker-compose.yml up -d app; \
		docker-compose -f docker-compose.yml logs -f app \
	'


.PHONY: talonify_be_services/stop
talonify_be_services/stop:
	docker-compose -f docker-compose.yml down


.PHONY: talonify_be_services/pytest
talonify_be_services/pytest: talonify_be_services/pytest/clean talonify_be_services/build-dev
	docker-compose -f docker-compose-pytest.yml up --build --abort-on-container-exit --exit-code-from pytest pytest; \
	EXIT_CODE=$$?; \
	make talonify_be_services/pytest/clean-flyway-status; \
	make talonify_be_services/pytest/clean; \
	exit $$EXIT_CODE


.PHONY: talonify_be_services/pytest/clean-full
talonify_be_services/pytest/clean-full:
	docker-compose -f docker-compose-pytest.yml down -v


.PHONY: talonify_be_services/pytest/clean-flyway-status
talonify_be_services/pytest/clean-flyway-status:
	docker-compose -f docker-compose-pytest.yml rm -sf flyway pytest; \
	docker volume rm -f flyway_status || true


.PHONY: talonify_be_services/pytest/clean
talonify_be_services/pytest/clean:
	docker-compose -f docker-compose-pytest.yml down --remove-orphans


.PHONY: talonify_be_services/build
talonify_be_services/build:
	${DOCKER_BUILD} --build-arg GITHASH=$(git rev-parse HEAD) -t ${DOCKER_REPO_NAME}:${ENVIRONMENT}_db_services_image -f deploy/Dockerfile .

################################################################################
# Flyway Migration
################################################################################

# Define the local path to flyway.conf file
LOCAL_FLYWAY_CONF := scripts/flyway_migrations/flyway.conf
