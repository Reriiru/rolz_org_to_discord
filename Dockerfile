FROM alpine:3.6

RUN apk add --no-cache python3 openssl-dev ca-certificates

ENV PROJECT_DIR /opt/bot
ENV APP_DIR $PROJECT_DIR/rolz_bot
ENV PYTHONPATH $PROJECT_DIR

WORKDIR $PROJECT_DIR
COPY setup.py $PROJECT_DIR
RUN pip3 install --no-cache-dir --upgrade pip setuptools && pip3 install --no-cache-dir pytest-runner && pip3 install --no-cache-dir -e $PROJECT_DIR

COPY ./rolz_bot $APP_DIR

EXPOSE 5000
CMD ["python3", "/opt/bot/rolz_bot/app.py"]
