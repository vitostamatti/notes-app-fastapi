install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black app/ && black tests/


lint:
	pylint --disable=R,C app/


test:
	python -m pytest -vv --cov=app/ tests


all: install format lint test