FROM python:3.9

WORKDIR /tmp

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./app /tmp/app

COPY ./database.sqlite /tmp/database.sqlite

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
