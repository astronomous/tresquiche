.PHONY: install run dev

install:
	pip install --upgrade -r requirements.txt

run:
	uvicorn main:app

dev:
	uvicorn main:app --reload
