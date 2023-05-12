FROM python:3.9-slim-bullseye

RUN apt -y update
RUN apt -y install gcc socat
RUN mkdir -p /codequest

COPY requirements/base.txt base.txt
COPY requirements/prod.txt requirements.txt
RUN pip install -r requirements.txt

ADD src /codequest/src
ADD maps /codequest/maps

WORKDIR /codequest

ENV USE_PYGAME 0

RUN echo 'python src/main.py "$@"' > run.sh
RUN chmod +x /codequest/run.sh

CMD ["/bin/sh", "-c", "./run.sh"]
