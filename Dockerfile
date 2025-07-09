# Use an official Python runtime as a parent image (Debian 12 "Bookworm" based)
FROM python:3.11-slim-bookworm

# Set environment variables to prevent generating .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the settings module for production
ENV DJANGO_SETTINGS_MODULE=cdcwaiv.settings.production

# --- Install System Dependencies for MS SQL Server ---
# Install prerequisites for adding new repositories
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    ca-certificates

# Add Microsoft's official repository GPG key
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

# Add the Microsoft repository for Debian 12 (Bookworm)
RUN curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install the ODBC driver and related development files
# The 'ACCEPT_EULA=Y' is required for the msodbcsql package
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 unixodbc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- Application Setup ---
# Create a non-root user for security
RUN addgroup --system app && adduser --system --group app

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
# Copy only the requirements file to leverage Docker's layer caching
COPY ./cdcwaiv/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# Install Gunicorn for serving the application
RUN pip install --no-cache-dir gunicorn

# Copy the Django project code into the container. The Django project root is the 'cdcwaiv' directory.
COPY ./cdcwaiv /app/

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "cdcwaiv.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]