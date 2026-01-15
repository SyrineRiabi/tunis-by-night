FROM python:3.9-slim

WORKDIR /app

# Copy requirements from the tests folder (since that's where you have them)
COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]