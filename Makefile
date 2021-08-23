.PHONY: deps server client

server:
	python muddy-server.py --migrate localhost 8080 ./world

client:
	python muddy-client.py cli ws://localhost:8080

client_script:
	python muddy-client.py cli --script=init_script.cmd ws://localhost:8080

2nd_account:
	python muddy-client.py cli --script=2nd_account.cmd ws://localhost:8080

deps:
	pip install -r requirements.txt
