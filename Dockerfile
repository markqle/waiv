FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_APP_DIR=/app/cdcwaiv

WORKDIR /app

# ODBC 18 for SQL Server
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl gnupg ca-certificates unixodbc unixodbc-dev \
  && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
     | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
     > /etc/apt/sources.list.d/mssql-release.list \
  && apt-get update && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
  && apt-get purge -y --auto-remove curl gnupg \
  && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /app/
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt \
 && pip install --no-cache-dir gunicorn

# App code (copy ENTIRE repo so /app/cdcwaiv/manage.py exists)
COPY . /app/

# Entrypoint
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && sed -i 's/\r$//' /app/entrypoint.sh

# Static/media dirs
RUN mkdir -p /app/staticfiles /app/media

# Non-root
RUN addgroup --system app && adduser --system --group app && chown -R app:app /app
USER app

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn","cdcwaiv.wsgi:application","--bind","0.0.0.0:8000","--workers","2","--timeout","60"]
