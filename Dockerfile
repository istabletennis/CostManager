# syntax=docker/dockerfile:1
FROM python:3.11-rc-bullseye
EXPOSE 5000
EXPOSE 5001
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["sh", "wrapper.sh"]

