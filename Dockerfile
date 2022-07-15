FROM python:3.8.10

RUN apt-get -y update && apt-get -y upgrade

COPY . /usr/app

WORKDIR /usr/app

RUN pip install -Ur requirements.txt

CMD [ "python3", "amore/bot.py" ]

