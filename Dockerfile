FROM python:3.9-alpine

RUN mkdir /src

COPY src/requirements.txt /src/requirements.txt

RUN pip3 install --no-cache-dir -r /src/requirements.txt

COPY src /src

WORKDIR /src

ENTRYPOINT ["python3", "main.py"]
