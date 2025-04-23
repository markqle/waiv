# waiv

Start project:
django-admin startproject waiv-cdc

Start app:
django-admin startapp waivapp

Add apps to settings (under INSTALLED APP):
'waivapp.apps.ApiConfig'

Whenever make changes to the model, database:
python manage.py makemigrations