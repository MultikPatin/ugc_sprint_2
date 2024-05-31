FROM python:3.11-slim

ENV SRC_PATH='/app' \
    APP_DIR='src/etl_analytics' \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR $SRC_PATH


COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --extras etl_analytics --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY ./${APP_DIR} ./${APP_DIR}
COPY ./src/core/__init__.py ./src/core/__init__.py
COPY ./src/core/configs/__init__.py ./src/core/configs/__init__.py
COPY ./src/core/utils/__init__.py ./src/core/utils/__init__.py
COPY ./src/core/utils/logger.py ./src/core/utils/logger.py

RUN sed -i 's/\r$//g' ${APP_DIR}/entrypoint.sh && \
    chmod +x ${APP_DIR}/entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "exec ${SRC_PATH}/${APP_DIR}/entrypoint.sh"]
