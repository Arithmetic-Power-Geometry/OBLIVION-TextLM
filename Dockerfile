FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md LICENSE NOTICE ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY docs ./docs
EXPOSE 8080
CMD ["uvicorn", "oblivion_textlm.api:app", "--host", "0.0.0.0", "--port", "8080"]
