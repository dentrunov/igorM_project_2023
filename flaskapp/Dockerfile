FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY . /myapp/flaskapp
WORKDIR /myapp/flaskapp
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
# ENTRYPOINT ["myapp/flaskapp/entrypoint.sh"]