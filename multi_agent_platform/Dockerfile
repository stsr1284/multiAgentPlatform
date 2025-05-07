FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./orchestration_app /code/orchestration_app
COPY ./plugin /code/plugin

CMD ["uvicorn", "main:app", "--app-dir", "orchestration_app", "--host", "0.0.0.0", "--port", "8080"]