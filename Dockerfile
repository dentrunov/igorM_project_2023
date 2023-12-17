FROM python:3.11
COPY . /myapp
WORKDIR /myapp 
RUN pip3 install -r requirements.txt
EXPOSE 5000