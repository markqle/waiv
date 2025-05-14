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

Working modules:
- Counselor : 
    - Login
    - Edit Student
    - Add Counseling session
    - View Profile
    - View dashboard
    - Log out
- Manager Employee (Program Coordinator / Director)
    - Login
    - Add Student (Referred from DOR / BMAC)
    - Edit Student
    - Add Staff
    - Manage Staff
    - Add Counseling session
    - Edit Counseling session
    - View Profile
    - View dashboard
    - Add monthly client listing
    - Add monthly report
    - Log out
- Admin:
    - Login
    - Add student
    - Add employee
    - Edit student
    - Remove student
    - View profile
    - View staff
    - Remove staff
    - Add counseling session
    - Edit counseling session
    - Remove counseling session
    - Add monthly client listing
    - Manage monthly client listing
    - Add monthly report
    - Manage monthly report
    - Log out


- For V2, handling adding files to the page: <br>
https://www.youtube.com/watch?v=lKyH_ZGtvwM