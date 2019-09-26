FROM python:3.7
ADD . /parking-citation
WORKDIR /parking-citation
RUN pip install -r requirements.txt
