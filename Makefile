.PHONY: up

up:
	docker compose up -d --build api
	docker compose logs -f api