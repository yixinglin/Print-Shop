FROM python:3.10.14-slim

ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install -y gcc libcups2-dev


RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 634

CMD ["python", "main.py"]