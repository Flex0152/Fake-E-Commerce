FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir . && \
    rm -rf /root/.cache

COPY dashboard_project/ .

VOLUME [ "/app/data" ] 

CMD ["python3", "app.py"]