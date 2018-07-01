FROM python:3.6.5-alpine

WORKDIR /srv/work/
ADD . /srv/work/
RUN pip3 install -e .

RUN addgroup -S zdict && adduser -S -G zdict zdict
USER zdict
WORKDIR /home/zdict

ENTRYPOINT ["zdict"]
