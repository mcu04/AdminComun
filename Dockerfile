FROM python:3.12.5-alpine3.20

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000

# Descomentar para produccion
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
