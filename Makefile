build:
	docker build -t light:latest .
run:
	docker run -d --name  lightcontainer --env-file "./src/.env" -p 9434:9434 -p 5432:5432 light

stop:
	docker stop lightcontainer

