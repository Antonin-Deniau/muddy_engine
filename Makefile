.PHONY: deps server client

server:
	python muddy-server.py --migrate localhost 8080 ./world

client:
	python muddy-client.py cli ws://localhost:8080

deps:
	pip install -r requirements.txt
