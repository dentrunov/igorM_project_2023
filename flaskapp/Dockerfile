FROM python:3.11
COPY . /myapp/flaskapp
WORKDIR /myapp/flaskapp
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 5000
# ENTRYPOINT ["myapp/flaskapp/entrypoint.sh"]