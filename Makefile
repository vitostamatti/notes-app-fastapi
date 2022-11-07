install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black app/ && black tests/


lint:
	pylint --disable=R,C app/


test:
	python -m pytest -vv --cov=app/ tests


build-image:
	python cli.py db-reset
	python cli.py db-init
	docker build . --tag notes-app-fastapi:latest  


run-image:
	docker run -d --name notes-app-fastapi-container -p 80:80 notes-app-fastapi


clean-image: 
	docker rm notes-app-fastapi-container