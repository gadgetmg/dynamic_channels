FROM python:alpine

WORKDIR /app

RUN pip3 install -U discord.py

COPY . .

CMD [ "python3", "bot.py" ]
