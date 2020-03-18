FROM python:3.7

RUN pip install python-telegram-bot
RUN pip install PySocks
RUN pip install pytz

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot.py
