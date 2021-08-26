.PHONY: deps server client

server:
	python muddy-server.py --migrate localhost 8080 ./world

client:
	python muddy-client.py cli ws://localhost:8080

1st_char:
	python muddy-client.py cli --script=1st_char.cmd ws://localhost:8080

2nd_char:
	python muddy-client.py cli --script=2nd_char.cmd ws://localhost:8080

deps:
	pip install -r requirements.txt
