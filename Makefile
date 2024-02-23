build:
	sudo docker compose up --build

stop:
	sudo docker compose down

logs:
	sudo docker compose logs -f