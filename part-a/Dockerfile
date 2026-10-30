
# Stage 1: Builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN groupadd -g 10001 app && useradd -u 10001 -g app -M app

COPY app.py .

USER 10001:10001

EXPOSE 8080

CMD ["waitress-serve", "--listen=0.0.0.0:8080", "app:app"]
