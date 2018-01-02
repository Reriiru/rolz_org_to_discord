FROM alpine:3.6

RUN apk add --no-cache python3

ADD docker/pip.conf /root/.pip/pip.conf

ENV PROJECT_DIR /opt/bot
ENV PYTHONPATH $PROJECT_DIR

WORKDIR $PROJECT_DIR
COPY setup.py $PROJECT_DIR
RUN pip3 install --no-cache-dir --upgrade pip setuptools && pip3 install --no-cache-dir -e $PROJECT_DIR

COPY ./rolz_bot $PROJECT_DIR

EXPOSE 5000
CMD ["python /opt/bot/app.py"]
