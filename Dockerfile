FROM python:3.8-alpine

WORKDIR /srv/work/
ADD . /srv/work/
RUN pip3 install -e .

RUN addgroup -S zdict && adduser -S -G zdict zdict
USER zdict
WORKDIR /home/zdict

ENTRYPOINT ["zdict"]
