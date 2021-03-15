FROM python:alpine

WORKDIR /app

RUN apk add build-base python3-dev libffi-dev
RUN pip3 install -U discord.py

COPY . .

CMD [ "python3", "bot.py" ]
