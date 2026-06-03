.PHONY: install init run dev clean

install:
	pip install --upgrade -r requirements.txt
	reflex init --template blank

init:
	reflex init --template blank

dev:
	reflex run --env dev

run:
	reflex run --env prod

clean:
	rm -rf .web __pycache__ */__pycache__
