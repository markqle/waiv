# waiv

Start project:
django-admin startproject waiv-cdc

Start app:
django-admin startapp waivapp

Add apps to settings (under INSTALLED APP):
'waivapp.apps.ApiConfig'

Whenever make changes to the model, database:
python manage.py makemigrations

Apply the migration:
python manage.py migrate

To change the DB from SQLite (default) to MySQL server:
Source: https://www.youtube.com/watch?v=4Nkr1K4yXJg
-> Change the credential from SQLite to MySQL
-> then you need to apply migrate
pip install mysqlclient

But your superuser credential will not migrate yet, you have to create new superuser for MySQL db 

THEN you need to go back to your SQLite to create the datadump.json from Django:
python manage.py dumpdata --exclude=contenttypes > datadump.json

THEN change credential to MySQL load that json in:
python manage.py loaddata datadump.json

test