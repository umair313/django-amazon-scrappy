SHELL=/bin/bash


cr_compose     := docker compose -f docker-compose.cr.yml
dev_compose    := docker compose -f docker-compose.dev.yml
success        := success

%.all: %.build %.up.d
	@echo $(success)

%.deploy: %.build %.down %.up.d %.migrate %.collectstatic
	@echo $(success)

%.build:
	@$($*_compose) build

%.up:
	@$($*_compose) up

%.up.d:
	@$($*_compose) up -d

%.down:
	@$($*_compose) down --remove-orphans

%.restart:
	@$($*_compose) restart

%.logs:
	@$($*_compose) logs -f

cr:
	@$($@_compose) up --build
	@$($@_compose) down

%.dcshell:
	@$($*_compose) exec django /bin/bash

%.sp:
	@$($*_compose) exec django python manage.py shell_plus

%.attach:
	@docker attach $*

%.makemigrations:
	@$($*_compose) exec django python manage.py makemigrations

%.migrate:
	@$($*_compose) exec django python manage.py migrate

%.collectstatic:
	@$($*_compose) exec django python manage.py collectstatic --noinput

%.psql:
	@$($*_compose) exec postgres psql -U postgres

%.rediscli:
	@$($*_compose) exec redis redis-cli -h redis
