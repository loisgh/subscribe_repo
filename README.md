How to Setup Subscriptions Application

1) git clone the repo to your server 
git@github.com:loisgh/subscribe_repo.git

2) Setup up your data base in settings.py
These settings are on lines 80 and 81 or settings.py

3) Run Django migrations:
This is done at the command line.  Make sure that you are in the base directory of your project.  
Make sure that manage.py is in the directory. 
The command for migrations is 

python manage.py migrate
If your migration runs correctly you will see the following lines

Running migrations:
  Applying subscribe_repo.0001_initial... OK
  Applying subscribe_repo.0002_auto_20210212_2319... OK
  Applying subscribe_repo.0003_auto_20210213_1624... OK
  Applying subscribe_repo.0004_auto_20210213_2107... OK

4) Run the Django Server: 
Also run at the command line

python manage.py runserver

5) Access the application: 
You can access the application using hostname:8000/subrepo/upload

6) If you wish to access the admin backend, create a username and password using the following command: python manage.py createsuperuser
You'll then be prompted for the information. 

7) Access the db backend using hostname:8000/admin