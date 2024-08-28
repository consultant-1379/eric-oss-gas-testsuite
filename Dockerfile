FROM armdocker.rnd.ericsson.se/sandbox/photon/ubuntu:20.04-py3.8

WORKDIR /testsuite
COPY ./testsuite/src/ /testsuite/
COPY ./requirements.txt /testsuite/
RUN pip3 install -r ./requirements.txt

RUN apt update && apt install -y firefox

ARG URL
ARG USERNAME
ARG PASSWORD
ENV URL_ENV=$URL
ENV USERNAME_ENV=$USERNAME
ENV PASSWORD_ENV=$PASSWORD
ENTRYPOINT python tests_runner.py $URL_ENV $USERNAME_ENV $PASSWORD_ENV
