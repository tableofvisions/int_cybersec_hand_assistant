FROM python:3.12-slim

RUN pip install uv

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml

COPY . .

RUN mkdir -p /app/data

COPY start.sh .
RUN chmod +x start.sh

CMD ["/app/start.sh"]
