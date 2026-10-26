FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt \
    && useradd --create-home --uid 10001 quizuser \
    && mkdir -p /app/data \
    && chown -R quizuser:quizuser /app

COPY --chown=quizuser:quizuser app.py before_lab1_questions.json between_lab1_and_lab2_questions.json ./
COPY --chown=quizuser:quizuser templates ./templates
COPY --chown=quizuser:quizuser static ./static

USER quizuser
EXPOSE 8000
CMD ["python", "app.py"]
