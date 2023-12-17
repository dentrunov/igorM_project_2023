FROM python:3.11
RUN apt-get update -y
RUN apt-get install -y python3
COPY . /app
WORKDIR /app 
RUN pip3 install --upgrade pip -r requirements.txt
EXPOSE 5000