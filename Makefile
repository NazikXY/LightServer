build:
	docker build -t light:latest .
run:
	docker run -d --env-file "./src/.env"  --name lightcontainer -p 9434:9434 -p 5432:5432 nazikxy/light:latest

stop:
	docker stop lightcontainer

