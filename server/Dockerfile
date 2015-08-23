FROM wikii122/python3:3.4.2
MAINTAINER Wiktor Ślęczka <wikii122@gmail.com>

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN rm requirements.txt

COPY server.py /srv/www/
COPY res /srv/www/res/

WORKDIR /srv/www/

CMD python3 server.py
