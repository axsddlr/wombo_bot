FROM python:3.8.12-slim-buster
LABEL maintainer="Andre Saddler <contact@rehkloos.com>"

# Download latest listing of available packages:
RUN apt-get -y update
# Upgrade already installed packages:
RUN apt-get -y upgrade

RUN apt-get -y install ffmpeg git

WORKDIR /wombot_art

RUN pip3 install --upgrade pip
RUN pip3 install virtualenv

COPY requirements.txt /wombo_art/requirements.txt


ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]
