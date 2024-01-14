FROM python:3.11
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY . /myapp/qr_reader
WORKDIR /myapp/qr_reader
RUN apt-get update && apt-get install libopencv-dev python3-opencv ffmpeg libsm6 libxext6  -y
# RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt
# ENTRYPOINT ["myapp/flaskapp/entrypoint.sh"]