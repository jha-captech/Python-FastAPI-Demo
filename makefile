run:
	@fastapi dev ./src/main.py

start-db:
	@colima start
	@docker compose up

stop-db:
	@colima start
	@docker compose down

reset-db:
	@colima start
	@docker compose down -v