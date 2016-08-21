FROM python:2-alpine

COPY . /dooblr

WORKDIR /dooblr

RUN pip install ./ 

ENTRYPOINT ["dooblr"]
