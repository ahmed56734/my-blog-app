# how to run project on localhost for windows users
make sure python is installed from www.python.org/ pip package manager should be installed by default

#open the cmd and run the following commands to setup your virtual environment

pip install virtualenv

pip install virtualenvwrapper-win

mkvirtualenv project

cd "THE-PATH-TO-THE-DOWNLOADED-PROJECT"\my-blog-app-master

setprojectdir .

pip install Flask

pip install flask-wtf

pip install flask-sqlalchemy

pip install flask-login

pip install flask-script

python manage.py runserver

open the browser and goto lacalhost:5000/

linux and mac users are supposed to be able to deal with this on their own :3 
