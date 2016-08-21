FROM python:2-alpine

COPY . /dooblr

WORKDIR /dooblr

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/dooblr/dooblr/main.py"]
