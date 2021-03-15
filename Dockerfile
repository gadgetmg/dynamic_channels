FROM python:alpine

WORKDIR /app

RUN apk add build-base ca-certificates libffi-dev python3-dev
RUN pip3 install -U discord.py

COPY . .

CMD [ "python3", "bot.py" ]
