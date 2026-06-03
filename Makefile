.PHONY: install run dev

install:
	pip install -r requirements.txt

run:
	uvicorn main:app

dev:
	uvicorn main:app --reload
