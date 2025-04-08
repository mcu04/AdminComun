FROM python:3.11.7-alpine3.19

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache \
    build-base \
    freetype-dev \
    libpng-dev \
    jpeg-dev \
    zlib-dev \
    gfortran \
    lapack-dev \
    musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
