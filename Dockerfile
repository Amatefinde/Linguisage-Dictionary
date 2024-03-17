FROM python:3.11
LABEL authors="Amatefinde"

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \

  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1


RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /linguisage
COPY poetry.lock pyproject.toml /linguisage/

RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

RUN poetry install


COPY . .
RUN mkdir "cert"
#COPY ../../../../etc/letsencrypt/live/linguisage.ru/fullchain.pem /linguisage/cert/fullchain.pem
#COPY ../../../../etc/letsencrypt/live/linguisage.ru/privkey.pem /linguisage/cert/privkey.pem


RUN chmod +x app_entry_point.sh

CMD ["/linguisage/app_entry_point.sh"]