FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV APP_HOME /app
ENV BUILD_ENV development

WORKDIR ${APP_HOME}

RUN addgroup --system django \
  && adduser --system --ingroup django django

RUN apt-get update \
  && apt-get install --no-install-recommends -y build-essential libpq-dev gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

#RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev

COPY ../entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY position_microservice ${APP_HOME}

#RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
#  && rm -rf /wheels/

RUN python3 -m pip install -r requirements.txt

RUN chown django:django ${APP_HOME}
RUN chown django:django ${APP_HOME}/db

USER django

ENTRYPOINT ["/entrypoint"]
