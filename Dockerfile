FROM python:3.8-alpine
LABEL maintainer="Andre Saddler <contact@rehkloos.com>"

LABEL build_date="2021-05-23"
RUN apk update && apk upgrade
RUN apk add --no-cache git make build-base linux-headers
RUN pip install virtualenv

WORKDIR /wombo_bot
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
