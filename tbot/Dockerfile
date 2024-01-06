FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY . /myapp/tbot
WORKDIR /myapp/tbot
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt