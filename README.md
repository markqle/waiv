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

IF we change too much schema and don't really have any data in current database:
rm your_app/migrations/*
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate

Install webpack for React:
npm i webpack webpack-cli --save-dev

Install babel - take the code and transpile into code that is friendly with all browsers:
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
npm install @babel/plugin-proposal-class-properties

Install React:
npm i react react-dom --save-dev
npm install react-router-dom

Install material UI - prebuilt component to style:
npm install @material-ui/core -- this fits react 16 or 17
npm install @mui/material @emotion/react @emotion/styled -- this fits later react like 18 and 19
npm install @mui/icons-material


Privilege:
- Admin
- IT
- Employee - Program Coordinator: allow "Add students"
- Employee: can only view students, edit student information, cannot add students

* Features & Module:
Staff Login:
- Add Student
- Staff Profile
- Add Counseling session
- Manage student
- Add document

Admin/Program Counselor Login
- Manage student
- Manage staff
- View Report / Dashboard
- Manage monthly client listing

Staff Working Module:
1. Login
2. View Profile
3. View Report / Dashboard
4. Add / View Counseling Note
5. View Student
6. Log out

Admin Login
1. Login
2. Add/ View Student
3. Add / View Staff
4. Remove Student
5. Remove Staff
6. Add / View Counseling Note
7. View Report / Dashboard
8. Add monthly client listing
9. Add document (optional)