SRV ?= telegram
PROJECT = github.com/icron/${SRV}
POD = `kubectl get -n telegram-app pods --selector=release=telegram-app -o jsonpath='{.items[0].metadata.name}'`

.PHONY: default
default: help

.PHONY: help
help: ## help information about make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-dev:
	@docker build \
		--build-arg PROJECT="${PROJECT}" \
		-t ${IMAGES} .
.PHONY: build-dev

restart: #restart uwsgi
	@kubectl -n telegram-app exec -it ${POD} supervisorctl restart uwsgi
	@kubectl -n telegram-app exec -it ${POD} supervisorctl restart cli
.PHONY: restart